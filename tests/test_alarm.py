import logging
from fireplan import Fireplan


def test_alarm_empty_data(requests_mock, caplog):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung",
        text="200",
        status_code=200,
    )
    fp = Fireplan("secret", "division")
    assert fp.alarm({}) is False
    assert requests_mock.call_count == 1
    assert "alle Werte leer" in caplog.text


def test_alarm_invalid_extra_data(requests_mock, caplog):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung",
        text="200",
        status_code=200,
    )
    fp = Fireplan("secret", "division")
    data = {
        "alarmtext": "Brand 3 –Brand im Wohnhaus",
        "einsatznrlst": "321123",
        "invalid": "ABC",
    }
    r = fp.alarm(data)
    assert r is True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == {
        "alarmtext": "Brand 3 –Brand im Wohnhaus",
        "einsatznrlst": "321123",
        "strasse": "",
        "hausnummer": "",
        "ort": "",
        "ortsteil": "",
        "objektname": "",
        "koordinaten": "",
        "einsatzstichwort": "",
        "zusatzinfo": "",
        "sonstiges1": "",
        "sonstiges2": "",
        "ric": "",
        "subric": "",
    }


def test_alarm_invalid_data_type(requests_mock, caplog):
    caplog.set_level(logging.INFO)
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung",
        text="200",
        status_code=200,
    )
    fp = Fireplan("secret", "division")
    r = fp.alarm({"ric": 123})
    assert r is False
    assert requests_mock.call_count == 1
    assert (
        "Validation error: ric, Input should be a valid string, value was 123"
        in caplog.text
    )


def test_alarm_invalid_coordinates(requests_mock, caplog):
    caplog.set_level(logging.INFO)
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung",
        text="200",
        status_code=200,
    )
    fp = Fireplan("secret", "division")
    r = fp.alarm({"koordinaten": "55,23 , 45,56"})
    assert r is False
    assert requests_mock.call_count == 1
    assert (
        r"Validation error: koordinaten, String should match pattern '^-?\d+\.\d+,\s?-?\d+\.\d+$', value was 55,23 , 45,56"
        in caplog.text
    )


def test_alarm_valid_data(requests_mock):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung",
        text="200",
        status_code=200,
    )
    fp = Fireplan("secret", "division")
    data = {
        "alarmtext": "Brand 3 –Brand im Wohnhaus",
        "einsatznrlst": "321123",
        "strasse": "Walter-Gropuius-Strasse",
        "hausnummer": "3",
        "ort": "München",
        "ortsteil": "Schwabing",
        "objektname": "Gebäude Kantine",
        "koordinaten": "51.3344,-5.22223",
        "einsatzstichwort": "Brand 5",
        "zusatzinfo": "Brandmeldeanlage",
        "sonstiges1": "sonstige1",
        "sonstiges2": "sonstige2",
        "ric": "40001",
        "subric": "A",
    }
    assert fp.alarm(data) is True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == data


def test_alarm_api_error(requests_mock, caplog):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung",
        text="400",
        status_code=400,
    )
    fp = Fireplan("secret", "division")
    data = {
        "alarmtext": "Brand 3 –Brand im Wohnhaus",
        "einsatznrlst": "321123",
    }
    assert fp.alarm(data) is False
    assert requests_mock.call_count == 2
    assert "Fehler beim senden des Alarms" in caplog.text
