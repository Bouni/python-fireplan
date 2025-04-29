from json import JSONDecodeError
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import Timeout

from fireplan import Fireplan


@pytest.fixture
def fireplan():
    return Fireplan("test-api-key")


@patch("fireplan.fireplan.requests.request")
def test_register_success(mock_request, fireplan):
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = {"utoken": "fake-api-token"}
    mock_request.return_value = mock_response

    result = fireplan.register("my-division")
    mock_request.assert_called_once_with(
        "GET",
        f"{fireplan.BASE_URL}Register/my-division",
        headers={"content-type": "application/json", "API-Key": "test-api-key"},
        timeout=5,
        json={},
    )
    assert result is True
    assert fireplan._apitoken == "fake-api-token"
    assert fireplan.headers["API-Token"] == "fake-api-token"


@patch("fireplan.fireplan.requests.request")
def test_register_failure(mock_request, fireplan):
    mock_response = MagicMock()
    mock_response.ok = False
    mock_request.return_value = mock_response

    result = fireplan.register("bad-division")
    assert result is False


@patch("fireplan.fireplan.requests.request")
def test_handle_request_timeout(mock_request, fireplan):
    mock_request.side_effect = Timeout("Timeout")
    result = fireplan._handle_request("GET", "some-endpoint")
    assert result == {}


@patch("fireplan.fireplan.requests.request")
def test_handle_request_json_decode_error(mock_request, fireplan):
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.side_effect = JSONDecodeError("Expecting value", "", 0)
    mock_request.return_value = mock_response

    result = fireplan._handle_request("GET", "bad-json")
    assert result == {}


def test_send_inbound_sms_not_implemented(fireplan, caplog):
    result = fireplan.send_inbound_sms({"message": "test"})
    assert result is False
    assert "Not implemented" in caplog.text


@patch("fireplan.fireplan.Fireplan._handle_request")
@patch("fireplan.fireplan.Fireplan._validate")
def test_send_alarm_success(mock_validate, mock_handle, fireplan):
    mock_validate.return_value = {"alarm": "data"}
    mock_handle.return_value = {"status": "ok"}

    result = fireplan.send_alarm({"alarm": "data"})
    assert result == {"status": "ok"}
    mock_validate.assert_called()
    mock_handle.assert_called()


@patch("fireplan.fireplan.Fireplan._handle_request")
@patch("fireplan.fireplan.Fireplan._validate")
def test_add_event_invalid_data(mock_validate, mock_handle, fireplan):
    mock_validate.return_value = {}
    mock_handle.return_value = {}
    result = fireplan.add_event({"invalid": "data"})
    assert result == {}
    mock_validate.assert_called_once()
    mock_handle.assert_called_once_with("POST", "Termine", {})


@patch("fireplan.fireplan.Fireplan._handle_request")
def test_get_operations_list(mock_handle, fireplan):
    mock_handle.return_value = {"operations": []}
    result = fireplan.get_operations_list(2024)
    assert result == {"operations": []}
    mock_handle.assert_called_once_with("GET", "Einsatzliste/2024")


@patch("fireplan.fireplan.Fireplan._handle_request")
def test_get_operations_log(mock_handle, fireplan):
    mock_handle.return_value = {"log": []}
    result = fireplan.get_operations_log("OP123", "HQ")
    assert result == {"log": []}
    mock_handle.assert_called_once_with(
        "GET", "Einsatztagebuch", headers={"EinsatzNrIntern": "OP123", "Standort": "HQ"}
    )


@patch("fireplan.fireplan.Fireplan._handle_request")
@patch("fireplan.fireplan.Fireplan._validate")
def test_add_operations_log(mock_validate, mock_handle, fireplan):
    mock_validate.return_value = {"log": "entry"}
    mock_handle.return_value = {"status": "ok"}
    result = fireplan.add_operations_log({"log": "entry"})
    assert result == {"status": "ok"}
    mock_validate.assert_called_once()
    mock_handle.assert_called_once_with("POST", "Einsatztagebuch", {"log": "entry"})


@patch("fireplan.fireplan.Fireplan._handle_request")
@patch("fireplan.fireplan.Fireplan._validate")
def test_set_fms_status(mock_validate, mock_handle, fireplan):
    mock_validate.return_value = {"status": "fms"}
    mock_handle.return_value = {"ok": True}
    result = fireplan.set_fms_status({"status": "fms"})
    assert result == {"ok": True}
    mock_validate.assert_called_once()
    mock_handle.assert_called_once_with("POST", "FMSStatus", {"status": "fms"})


@patch("fireplan.fireplan.Fireplan._handle_request")
def test_get_calendar(mock_handle, fireplan):
    mock_handle.return_value = {"calendar": "data"}
    result = fireplan.get_calendar()
    assert result == {"calendar": "data"}
    mock_handle.assert_called_once_with("GET", "Kalender")


@patch("fireplan.fireplan.Fireplan._handle_request")
def test_get_other_services(mock_handle, fireplan):
    mock_handle.return_value = {"services": []}
    result = fireplan.get_other_services(2025)
    assert result == {"services": []}
    mock_handle.assert_called_once_with("GET", "SonstigeDienste/2025")


@patch("fireplan.fireplan.Fireplan._handle_request")
def test_get_events(mock_handle, fireplan):
    mock_handle.return_value = {"events": []}
    result = fireplan.get_events(42)
    assert result == {"events": []}
    mock_handle.assert_called_once_with("GET", "Termine/42")


@patch("fireplan.fireplan.Fireplan._handle_request")
@patch("fireplan.fireplan.Fireplan._validate")
def test_add_event(mock_validate, mock_handle, fireplan):
    mock_validate.return_value = {"event": "data"}
    mock_handle.return_value = {"result": "ok"}
    result = fireplan.add_event({"event": "data"})
    assert result == {"result": "ok"}
    mock_validate.assert_called_once()
    mock_handle.assert_called_once_with("POST", "Termine", {"event": "data"})
