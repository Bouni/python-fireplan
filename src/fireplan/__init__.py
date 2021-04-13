import logging
import requests
import cerberus
from fireplan.schemas import ALARM_SCHEMA, STATUS_SCHEMA

logger = logging.getLogger(__name__)


class Fireplan:

    BASE_URL = "https://fireplanapi.azurewebsites.net/api/"

    def __init__(self, secret, division):
        self._secret = secret
        self._division = division
        self._token = None
        self.headers = {
            "utoken": None,
            "content-type": "application/json",
        }
        self._get_token()
        self.validator = cerberus.Validator(purge_unknown=True)

    def _get_token(self):
        url = f"{self.BASE_URL}registerV2"
        headers = {
            "cxsecret": self._secret,
            "abteilung": self._division,
        }
        r = requests.get(url, headers=headers)
        if r.status_code == requests.codes.ok:
            logger.info(f"User Token erfolgreich generiert!")
            self.headers["utoken"] = r.text
        else:
            logger.error(f"Fehler beim generieren des User Token!")
            logger.error(r.text)

    def alarm(self, data):
        url = f"{self.BASE_URL}Alarmierung"
        self.validator.validate(data, ALARM_SCHEMA, update=True)
        data = self.validator.document
        self.validator.validate(data, ALARM_SCHEMA)
        for error in self.validator.errors:
            logger.warning(
                f"Fehler in den Alarmdaten, '{error}' ist falsch formatiert und wird daher auf \"\" gesetzt!"
            )
            data[error] = ""
        logger.debug(data)
        r = requests.post(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Alarm erfolgreich gesendet")
        else:
            logger.error("Fehler beim senden des Alarms")
            logger.error(f"Status code: {r.status_code}")
            logger.error(f"Error text: {r.text}")
        return r.text == "200"

    def status(self, data):
        url = f"{self.BASE_URL}FMS"
        logger.info(f"input data: {data}")
        valid = self.validator.validate(data, STATUS_SCHEMA)
        logger.info(f"validation: {valid}")
        logger.info(f"document: {self.validator.document}")
        for error in self.validator.errors:
            logger.warning(
                f"Fehler in den Statusdaten, der Wert von '{error}' ist ungültig!"
            )
        if self.validator.errors:
            logger.error(
                f"Status übermittlung auf Grund fehlerhafter daten abgebrochen!"
            )
            return
        logger.debug(data)
        r = requests.put(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Status erfolgreich gesendet")
        else:
            logger.error("Fehler beim senden des Status")
            logger.error(f"Status code: {r.status_code}")
            logger.error(f"Error text: {r.text}")
        return r.text == "200"
