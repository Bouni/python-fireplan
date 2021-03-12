import logging
import string
import random
import fireplan


def test_status_empty_data(requests_mock):
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("token")
    assert fp.status({}) == True
    assert requests_mock.called
    assert requests_mock.last_request.json() == {
        "FZKennung": "",
        "Status": "",
    }


def test_status_invalid_extra_data(requests_mock, logs):
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("token")
    r = fp.status({"invalid": "ABC"})
    assert r == None
    assert requests_mock.called == False
    assert "extra keys not allowed" in logs.error


def test_status_invalid_data_type(requests_mock, logs):
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("token")
    r = fp.status({"Status": 12})
    assert r == None
    assert requests_mock.called == False
    assert "expected str for dictionary value" in logs.error


def test_status_valid_data(requests_mock):
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("token")
    data = {"FZKennung": "40225588996", "Status": "3"}
    assert fp.status(data) == True
    assert requests_mock.called
    assert requests_mock.last_request.json() == data


def test_status_api_error(requests_mock):
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="400")
    fp = fireplan.Fireplan("token")
    assert fp.status({}) == False
    assert requests_mock.called
