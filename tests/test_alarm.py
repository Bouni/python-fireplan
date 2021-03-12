import logging
import string
import random
import fireplan


def test_alarm_empty_data(requests_mock):
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("token")
    assert fp.alarm({}) == True
    assert requests_mock.called
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
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("token")
    r = fp.alarm({"invalid": "ABC"})
    assert r == None
    assert requests_mock.called == False
    assert "extra keys not allowed" in logs.error


def test_alarm_invalid_data_type(requests_mock, logs):
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("token")
    r = fp.alarm({"RIC": 12})
    assert r == None
    assert requests_mock.called == False
    assert "expected str for dictionary value" in logs.error


def test_alarm_invalid_coordinates(requests_mock, logs):
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("token")
    r = fp.alarm({"koordinaten": "55,23 , 45,56"})
    assert r == None
    assert requests_mock.called == False
    assert "wrong format, must be like" in logs.error


def test_alarm_valid_data(requests_mock):
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="200"
    )
    fp = fireplan.Fireplan("token")
    data = {
        "alarmtext": "Brand 3 –Brand im Wohnhaus",
        "einsatznrlst": "321123",
        "strasse": "Walter-Gropuius-Strasse",
        "hausnummer": "3",
        "ort": "München",
        "ortsteil": "Schwabing",
        "objektname": "Gebäude Kantine",
        "koordinaten": "51.3344,65.22223",
        "einsatzstichwort": "Brand 5",
        "zusatzinfo": "Brandmeldeanlage",
        "sonstiges1": "sonstige1",
        "sonstiges2": "sonstige2",
        "RIC": "40001",
        "SubRIC": "A",
    }
    assert fp.alarm(data) == True
    assert requests_mock.called
    assert requests_mock.last_request.json() == data


def test_alarm_api_error(requests_mock):
    requests_mock.post(
        "https://fireplanapi.azurewebsites.net/api/Alarmierung", text="400"
    )
    fp = fireplan.Fireplan("token")
    assert fp.alarm({}) == False
    assert requests_mock.called
