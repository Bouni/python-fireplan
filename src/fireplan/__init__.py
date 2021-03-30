import logging
import requests
import cerberus
from fireplan.schemas import ALARM_SCHEMA, STATUS_SCHEMA

logger = logging.getLogger(__name__)

class Fireplan:

    BASE_URL = "https://fireplanapi.azurewebsites.net/api/"

    def __init__(self, token):
        self.token = token
        self.headers = {
            "utoken": token,
            "content-type": "application/json",
        }
        self.validator = cerberus.Validator()

    def alarm(self, data):
        url = f"{self.BASE_URL}Alarmierung"
        self.validator.validate(data, ALARM_SCHEMA, update=True)
        data = self.validator.document
        self.validator.validate(data, ALARM_SCHEMA)
        for error in self.validator.errors:
            logger.warning(f"Fehler in den Alarmdaten, '{error}' ist falsch formatiert und wird daher auf \"\" gesetzt!")
            data[error] = ""
        r = requests.post(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Alarm erfolgreich gesendet")
        else:
            logger.error("Fehler beim senden des Alarms")
        return r.text == "200"

    def status(self, data):
        url = f"{self.BASE_URL}FMS"
        logger.info(f"input data: {data}")
        valid = self.validator.validate(data, STATUS_SCHEMA)
        logger.info(f"validation: {valid}")
        logger.info(f"document: {self.validator.document}")
        for error in self.validator.errors:
            logger.warning(f"Fehler in den Statusdaten, der Wert von '{error}' ist ungültig!")
        if self.validator.errors:
            logger.error(f"Status übermittlung auf Grund fehlerhafter daten abgebrochen!")
            return
        r = requests.put(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Status erfolgreich gesendet")
        else:
            logger.error("Fehler beim senden des Status")
            logger.error(r.text)
        return r.text == "200"
