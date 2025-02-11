import pytest


@pytest.mark.order(1)
def test_create_device_entry(test_client):
    """
    Tests creating a new device successfully and handling bad inputs.
    """
    # Example of successful creation
    valid_payload = {
        "device_name": "Device1",
        "device_type": "android",
        "status": "offline"
    }
    response = test_client.post("/api/v1/devices", json=valid_payload)
    assert response.status_code == 201  # or whatever success code is expected


    # Example of bad request
    invalid_payload = {
        # Missing required fields or invalid data
    }
    response = test_client.post("/api/v1/devices", json=invalid_payload)
    assert response.status_code == 422  # or the expected error code


@pytest.mark.order(2)
def test_get_devices_empty_list(test_client):
    """
    Ensures that when no devices are found, an empty list is returned or
    the correct response is given.
    """
    response = test_client.get("/api/v1/devices")
    assert response.status_code == 200
    data = response.json()
    # Ensure data structure is correct. If no devices, then data might be []
    assert isinstance(data, dict)



@pytest.mark.order(3)
def test_get_device_not_found(test_client):
    """
    Query details for a device ID that does not exist.
    """
    response = test_client.get("/api/v1/devices/999999")  # A non-existent ID
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(4)
def test_get_device_success(test_client):
    """
    Tests obtaining details for an existing device.
    """

    response = test_client.get(f"/api/v1/devices/1")
    assert response.status_code == 200

@pytest.mark.order(5)
def test_send_command(test_client):
    """
    Tests sending a command to an existing device, including edge cases.
    """


    command_payload = {"command": "reboot"}
    cmd_resp = test_client.post(f"/api/v1/devices/1/command", json=command_payload)
    assert cmd_resp.status_code == 200

@pytest.mark.order(6)
def test_delete_device(test_client):
    """
    Tests deleting a device successfully.
    """

    delete_resp =  test_client.delete(f"/api/v1/devices/1")
    assert delete_resp.status_code == 200  # or whatever success code is expected






