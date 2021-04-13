import logging
import string
import random
import fireplan


def test_alarm_empty_data(requests_mock):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("secret", "division")
    assert fp.alarm({}) == True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == {
        "alarmtext": "",
        "einsatznrlst": "",
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
        "RIC": "",
        "SubRIC": "",
    }


def test_alarm_invalid_extra_data(requests_mock, logs):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("secret", "division")
    r = fp.alarm({"invalid": "ABC"})
    assert r == True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == {
        "alarmtext": "",
        "einsatznrlst": "",
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
        "RIC": "",
        "SubRIC": "",
    }


def test_alarm_invalid_data_type(requests_mock, logs):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("secret", "division")
    r = fp.alarm({"RIC": 123})
    assert r == True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == {
        "alarmtext": "",
        "einsatznrlst": "",
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
        "RIC": "123",
        "SubRIC": "",
    }


def test_alarm_invalid_coordinates(requests_mock, logs):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("secret", "division")
    r = fp.alarm({"koordinaten": "55,23 , 45,56"})
    assert r == True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == {
        "alarmtext": "",
        "einsatznrlst": "",
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
        "RIC": "",
        "SubRIC": "",
    }


def test_alarm_valid_data(requests_mock):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("secret", "division")
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
        "RIC": "40001",
        "SubRIC": "A",
    }
    assert fp.alarm(data) == True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == {
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
        "RIC": "40001",
        "SubRIC": "A",
    }


def test_alarm_api_error(requests_mock):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="400"
    )
    fp = fireplan.Fireplan("secret", "division")
    assert fp.alarm({}) == False
    assert requests_mock.call_count == 2
