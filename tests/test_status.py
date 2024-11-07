import fireplan


def test_status_empty_data(requests_mock, caplog):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({}) is False
    assert requests_mock.call_count == 1
    assert "alle Werte leer" in caplog.text


def test_status_invalid_extra_data(requests_mock, caplog):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({"invalid": "ABC"}) is False
    assert requests_mock.call_count == 1
    assert "alle Werte leer" in caplog.text


def test_status_invalid_data_type(requests_mock, caplog):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({"Status": 12}) is False
    assert requests_mock.call_count == 1


def test_status_valid_data(requests_mock):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="200")
    fp = fireplan.Fireplan("secret", "division")
    data = {
        "fzKennung": "40225588996",
        "status": "3",
        "statusTime": "2024-11-06T13:47:05.347Z",
    }
    assert fp.status(data) is True
    assert requests_mock.call_count == 2
    assert requests_mock.last_request.json() == data


def test_status_api_error(requests_mock):
    requests_mock.get(
        "https://fireplanapi.azurewebsites.net/api/registerV2", text="token"
    )
    requests_mock.put("https://fireplanapi.azurewebsites.net/api/FMS", text="400")
    fp = fireplan.Fireplan("secret", "division")
    assert fp.status({}) is False
    assert requests_mock.call_count == 1
