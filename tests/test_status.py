import logging
import string
import random
import fireplan


def test_status_empty_data(requests_mock):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({}) == None
    assert requests_mock.call_count == 1


def test_status_invalid_extra_data(requests_mock, logs):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({"invalid": "ABC"}) == None
    assert requests_mock.call_count == 1


def test_status_invalid_data_type(requests_mock, logs):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({"Status": 12}) == None
    assert requests_mock.call_count == 1


def test_status_valid_data(requests_mock):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    data = {"FZKennung": "40225588996", "Status": "3"}
    assert fp.status(data) == True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == data


def test_status_api_error(requests_mock):
    requests_mock.get("https://fireplanapi.azurewebsites.net/api/registerV2", text="token")
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="400")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({}) == None
    assert requests_mock.call_count == 1
