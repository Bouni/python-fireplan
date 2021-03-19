import logging
import requests
import voluptuous as v

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class Fireplan:

    BASE_URL = "https://fireplanapi.azurewebsites.net/api/"
    ALARM_SCHEMA = v.Schema(
        {
            v.Required("alarmtext", default=""): str,
            v.Required("einsatznrlst", default=""): str,
            v.Required("strasse", default=""): str,
            v.Required("hausnummer", default=""): str,
            v.Required("ort", default=""): str,
            v.Required("ortsteil", default=""): str,
            v.Required("objektname", default=""): str,
            v.Required("koordinaten", default=""): v.Any(
                v.Match(
                    r"^\d+\.\d+,\d+\.\d+$",
                    msg="wrong format, must be like 47.592,8.298",
                ),
                v.Match(r"^$"),
            ),
            v.Required("einsatzstichwort", default=""): str,
            v.Required("zusatzinfo", default=""): str,
            v.Required("sonstiges1", default=""): str,
            v.Required("sonstiges2", default=""): str,
            v.Required("RIC", default=""): str,
            v.Required("SubRIC", default=""): str,
        }
    )
    STATUS_SCHEMA = v.Schema(
        {
            v.Required("FZKennung", default=""): str,
            v.Required("Status", default=""): str,
        }
    )

    def __init__(self, token):
        self.token = token
        self.headers = {
            "utoken": token,
            "content-type": "application/json",
        }

    def alarm(self, data):
        url = f"{self.BASE_URL}Alarmierung"
        try:
            data = self.ALARM_SCHEMA(data)
        except Exception as e:
            logger.error(e)
            return
        r = requests.post(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Alarm erfolgreich gesendet")
        else:
            logger.error("Fehler beim senden des Alarms")
        return r.text == "200"

    def status(self, data):
        url = f"{self.BASE_URL}FMS"
        try:
            data = self.STATUS_SCHEMA(data)
        except Exception as e:
            logger.error(e)
            return
        r = requests.put(url, json=data, headers=self.headers)
        if r.text == "200":
            logger.info("Status erfolgreich gesendet")
        else:
            logger.error("Fehler beim senden des Status")
            logger.error(r.text)
        return r.text == "200"
