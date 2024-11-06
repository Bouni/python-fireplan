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
        logger.debug(f"Initialisierung mit Registration ID {secret} und Abteilung {division}")
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
        if r.status_code == requests.codes.ok and r.text:
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
        logger.debug("Alarmdaten:")
        logger.debug(data)
        r = requests.post(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Alarm erfolgreich gesendet")
            logger.info(f"Status code: {r.status_code}")
            logger.info(f"Text: {r.text}")
        else:
            logger.error("Fehler beim senden des Alarms")
            logger.error(f"Status code: {r.status_code}")
            logger.error(f"Error text: {r.text}")
        return r.ok

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
                "Status übermittlung auf Grund fehlerhafter Daten abgebrochen!"
            )
            return
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
