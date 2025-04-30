import logging
from json import JSONDecodeError
from pprint import pformat

import requests
from pydantic import BaseModel, ValidationError

from fireplan.models import (
    AlarmDataModel,
    EventDataModel,
    FMSStatusDataModel,
    OperationDataModel,
)

logger = logging.getLogger(__name__)


class Fireplan:
    """A wrapper for the public fireplan API."""

    BASE_URL = "https://data.fireplan.de/api/"

    def __init__(self, apikey: str):
        self._apikey = apikey
        self._apitoken = None
        self.headers = {
            "content-type": "application/json",
        }

    @staticmethod
    def _log_api_result(label: str):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                data = func(self, *args, **kwargs)
                logger.debug("[%s]\n%s", label, pformat(data))
                return data

            return wrapper

        return decorator

    def _handle_request(
        self, method: str, endpoint: str, data: dict = {}, headers: dict = {}
    ) -> dict | bool:
        """Send a post request to the Fireplan API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(
                method, url, headers={**self.headers, **headers}, timeout=5, json=data
            )
        except requests.exceptions.Timeout as err:
            logger.error(f"Timout beim senden: {err}")
            return {}
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error: {err}")
            return {}
        except requests.exceptions.JSONDecodeError as err:
            logger.error(f"JSON decoder error: {err}")
            return {}
        except requests.exceptions.RequestException as err:
            logger.error(f"Etwas ist schief gelaufen: {err}")
            return {}
        if response.ok:
            self._log_result(endpoint, response)
            try:
                return response.json()
            except JSONDecodeError:
                return {}
        else:
            return False

    def _log_result(self, endpoint: str, response: requests.Response) -> None:
        """Print log message depending on response."""
        if response:
            logger.info(f"[{endpoint}] Senden erfolgreich")
            logger.info(f"[{endpoint}] Status code: {response.status_code}")
        else:
            logger.error(f"[{endpoint}] Fehler beim senden")
            logger.error(f"[{endpoint}] Status code: {response.status_code}")
            logger.error(f"[{endpoint}] Error text: {response.text}")

    def _validate(self, raw_data: dict, model: type[BaseModel]) -> dict:
        """Validate raw data with a given model."""
        try:
            data = model(**raw_data)
            data = data.model_dump()
        except ValidationError as e:
            for error in e.errors():
                logger.error(
                    f"Validation error: {error['loc'][0]}, {error['msg']}, value was {error['input']}"
                )
            return {}
        if not any(data.values()):
            logger.error("Keine nutzbaren Daten")
            return {}
        return data

    def register(self, division: str) -> bool:
        """Register a division and get an API key for it."""
        data = self._handle_request(
            "GET", f"Register/{division}", headers={"API-Key": self._apikey}
        )
        if not isinstance(data, bool):
            self._apitoken = data["utoken"]
            self.headers["API-Token"] = self._apitoken
            return True
        return False

    @_log_api_result("Alarmierung")
    def send_alarm(self, data: dict) -> dict | bool:
        """Send alarm data to the API."""
        data = self._validate(data, AlarmDataModel)
        return self._handle_request("POST", "Alarmierung", data)

    @_log_api_result("Einsatzliste")
    def get_operations_list(self, year: int) -> dict | bool:
        """Get list of operations for a given year from the API."""
        return self._handle_request("GET", f"Einsatzliste/{year}")

    @_log_api_result("Einsatztagebuch")
    def get_operations_log(self, operation_number: str, location: str) -> dict | bool:
        """Get operation log for a given operation number and location."""
        data = self._handle_request(
            "GET",
            "Einsatztagebuch",
            headers={"EinsatzNrIntern": operation_number, "Standort": location},
        )
        return data

    @_log_api_result("Einsatztagebuch")
    def add_operations_log(self, data: dict) -> dict | bool:
        """Add an operation log."""
        data = self._validate(data, OperationDataModel)
        return self._handle_request("POST", "Einsatztagebuch", data)

    @_log_api_result("FMSStatus")
    def set_fms_status(self, data: dict) -> dict | bool:
        """Set the FMS status for a vehicle."""
        data = self._validate(data, FMSStatusDataModel)
        return self._handle_request("POST", "FMSStatus", data)

    @_log_api_result("Kalender")
    def get_calendar(self) -> dict | bool:
        """Get calendar from the API."""
        data = self._handle_request("GET", "Kalender")
        return data

    def send_inbound_sms(self, data: dict) -> bool:
        """Send inbound SMS data to the API."""
        logger.warning("Not implemented")
        return False

    @_log_api_result("SonstigeDienste")
    def get_other_services(self, year: int) -> dict | bool:
        """Get other services for a given year from the API."""
        data = self._handle_request("GET", f"SonstigeDienste/{year}")
        return data

    @_log_api_result("Termine")
    def get_events(self, calendar_id: int) -> dict | bool:
        """Get all events from a calendar by its ID."""
        data = self._handle_request("GET", f"Termine/{calendar_id}")
        return data

    @_log_api_result("Termine")
    def add_event(self, data: dict) -> dict | bool:
        """Add an event to a calendar via the API."""
        data = self._validate(data, EventDataModel)
        return self._handle_request("POST", "Termine", data)
