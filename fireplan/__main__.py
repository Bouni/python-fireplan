import logging
from pprint import pformat

import requests
from pydantic import BaseModel, ValidationError

from fireplan.models import AlertDataModel, FMSStatusDataModel, OperationDataModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


class Fireplan:
    """A wrapper for the public fireplan API."""

    BASE_URL = "https://data.fireplan.de/api/"

    def __init__(self, apitoken: str, division: str, registration_id: str):
        self._division = division
        if apitoken:
            logger.debug(
                f"Initialisierung mit API-TOKEN '{apitoken}' und Abteilung '{division}'"
            )
            self._apitoken = apitoken
        else:
            self._apitoken = self._get_token(registration_id, self._division)
        self.headers = {
            "API-Token": self._apitoken,
            "content-type": "application/json",
        }

    def _get_token(self, secret: str, division: str) -> str:
        """Retrieve API token, this is a hacky solution for the moment."""
        url = "https://fireplanapi.azurewebsites.net/api/registerV2"
        headers = {
            "cxsecret": secret,
            "abteilung": division,
        }
        r = requests.get(url, headers=headers)
        if r.ok:
            logger.info("User Token erfolgreich generiert!")
            # This is a hack because we get the token back wrapped in ""
            if r.text.startswith('"'):
                token = r.text[1:-1]
            else:
                token = r.text
            self._log_token(token)
            return token
        else:
            logger.error("Fehler beim generieren des User Token!")
            logger.error(r.status_code)
            logger.error(r.text)
            return ""

    def _log_object(self, label: str, obj: dict):
        logger.info("%s\n\n\n%s\n\n", label, pformat(obj, compact=True))

    def _log_token(self, token: str):
        logger.info("%s...%s}", token[:32], token[-32:])

    def _get(self, endpoint: str, headers: dict = {}) -> dict:
        """Send a post request to the Fireplan API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            r = requests.get(url, headers={**self.headers, **headers}, timeout=1)
        except requests.exceptions.Timeout as err:
            logger.error(f"Timout beim senden: {err}")
            return {}
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error: {err}")
            return {}
        except requests.exceptions.RequestException as err:
            logger.error(f"Etwas ist schief gelaufen: {err}")
            return {}
        self._log_result(r)
        return r.json()

    def _post(self, endpoint: str, data: dict) -> bool:
        """Send a post request to the Fireplan API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            r = requests.post(url, json=data, headers=self.headers, timeout=1)
        except requests.exceptions.Timeout as err:
            logger.error(f"Timout beim senden: {err}")
            return False
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error: {err}")
            return False
        except requests.exceptions.RequestException as err:
            logger.error(f"Etwas ist schief gelaufen: {err}")
            return False
        self._log_result(r)
        return True

    def _log_result(self, response: requests.Response) -> None:
        """Print log message depending on response."""
        if response:
            logger.info("Senden erfolgreich")
            logger.info(f"Status code: {response.status_code}")
        else:
            logger.error("Fehler beim senden")
            logger.error(f"Status code: {response.status_code}")
            logger.error(f"Error text: {response.text}")

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

    def send_alert(self, data: dict) -> bool:
        """Send alert data to the API."""
        endpoint = "Alarmierung"
        data = self._validate(data, AlertDataModel)
        return self._post(endpoint, data)

    def get_operations_list(self, year: int) -> dict:
        """Get list of operations for a given year from the API."""
        endpoint = f"Einsatzliste/{year}"
        data = self._get(endpoint)
        self._log_object("Einsatzliste", data)
        return data

    def get_operations_log(self, operation_number: str, location: str) -> dict:
        """Get opeartion log for a given operation number and location."""
        endpoint = "Einsatztagebuch"
        headers = {"EinsatzNrIntern": operation_number, "Standort": location}
        data = self._get(endpoint, headers=headers)
        self._log_object("Einsatztagebuch", data)
        return data

    def add_operations_log(self, data: dict) -> bool:
        """Add an operation log."""
        endpoint = "Einsatztagebuch"
        data = self._validate(data, OperationDataModel)
        return self._post(endpoint, data)

    def set_fms_status(self, data: dict) -> bool:
        """Set the FMS status for a vehicle."""
        endpoint = "FMSStatus"
        data = self._validate(data, FMSStatusDataModel)
        return self._post(endpoint, data)

    def get_calendar(self) -> dict:
        """Get calendar from the API."""
        endpoint = "Kalender"
        data = self._get(endpoint)
        self._log_object("Kalender", data)
        return data

    def register(self, division:str) -> dict:
        """Register a division and get an API key for it."""
        endpoint = f"Register/{division}"
        data = self._get(endpoint)
        self._log_object("Register", data)
        return data



if __name__ == "__main__":
    fp = Fireplan("", "Kuessaberg", "624A5526-39B75C4B")
    # fp.get_operations_list(2024)
    fp.get_calendar()
    # fp.send_alert(
    #     {
    #         "ric": "string",
    #         "subRIC": "string",
    #         "einsatznrlst": "string",
    #         "strasse": "string",
    #         "hausnummer": "string",
    #         "ort": "string",
    #         "ortsteil": "string",
    #         "objektname": "string",
    #         "koordinaten": "string",
    #         "einsatzstichwort": "string",
    #         "zusatzinfo": "string",
    #     }
    # )
