import logging
import requests
from pydantic import ValidationError
from fireplan.models import AlarmdataModel, StatusdataModel

logger = logging.getLogger(__name__)


class Fireplan:
    """A wrapper for the public fireplan API."""

    BASE_URL = "https://fireplanapi.azurewebsites.net/api/"

    def __init__(self, secret, division):
        self._secret = secret
        self._division = division
        logger.debug(
            f"Initialisierung mit Registration ID {secret} und Abteilung {division}"
        )
        self.headers = {
            "utoken": None,
            "content-type": "application/json",
        }
        self._get_token()

    def _get_token(self) -> None:
        """Retrieve API token."""
        url = f"{self.BASE_URL}registerV2"
        headers = {
            "cxsecret": self._secret,
            "abteilung": self._division,
        }
        r = requests.get(url, headers=headers)
        if r.ok:
            logger.info("User Token erfolgreich generiert!")
            logger.debug(f"Token: {r.text}")
            # This is a hack because we get the token back wrapped in ""
            if r.text.startswith('"'):
                self.headers["utoken"] = r.text[1:-1]
            else:
                self.headers["utoken"] = r.text
            logger.debug(f"Headers: {self.headers}")
        else:
            logger.error("Fehler beim generieren des User Token!")
            logger.error(r.status_code)
            logger.error(r.text)

    def alarm(self, data: dict) -> bool:
        """Send alarm data to the API."""
        url = f"{self.BASE_URL}Alarmierung"
        try:
            data = AlarmdataModel(**data)
            data = data.model_dump()
        except ValidationError as e:
            for error in e.errors():
                logger.info(
                    f"Validation error: {error['loc'][0]}, {error['msg']}, value was {error['input']}"
                )
            logger.error("Alarm übermittlung auf Grund fehlerhafter Daten abgebrochen!")
            return False
        if not any(data.values()):
            logger.error("Alarm übermittlung abgebrochen da alle Werte leer sind!")
            return False
        logger.debug("Alarmdaten:")
        logger.debug(data)
        r = requests.post(url, json=data, headers=self.headers)
        if r.ok:
            logger.info("Alarm erfolgreich gesendet")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Text: {r.text}")
        else:
            logger.error("Fehler beim senden des Alarms")
            logger.error(f"Status code: {r.status_code}")
            logger.error(f"Error text: {r.text}")
        return r.ok

    def status(self, data: dict) -> bool:
        """Send FMS status data to the API."""
        url = f"{self.BASE_URL}FMS"
        try:
            data = StatusdataModel(**data)
            data = data.model_dump()
        except ValidationError as e:
            for error in e.errors():
                logger.info(
                    f"Validation error: {error['loc'][0]}, {error['msg']}, value was {error['input']}"
                )
            logger.error(
                "Status übermittlung auf Grund fehlerhafter Daten abgebrochen!"
            )
            return False
        if not any(data.values()):
            logger.error("Status übermittlung abgebrochen da alle Werte leer sind!")
            return False
        logger.debug("Statusdaten:")
        logger.debug(data)
        r = requests.put(url, json=data, headers=self.headers)
        if r.ok:
            logger.info("Status erfolgreich gesendet")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Text: {r.text}")
        else:
            logger.error("Fehler beim senden des Status")
            logger.error(f"Status code: {r.status_code}")
            logger.error(f"Error text: {r.text}")
        return r.ok
