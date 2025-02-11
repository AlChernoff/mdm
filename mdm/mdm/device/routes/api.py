import asyncio

from mdm.device.services.websockets_service import connect_websocket, handle_websocket_messages, notify_device_change
from mdm.logging_config import logger

from fastapi import APIRouter, Response, status, WebSocket, WebSocketDisconnect

from mdm.database import DBSessionDep
from mdm.device.models.device_request import (
    DeviceGetModel,
    DeviceRequestModel,
    GetDeviceResponseModel,
    GetDevicesResponseModel,
    PutDeviceResponseModel, CommandRequestModel, PutDeviceRequestModel,
)
from mdm.device.services.device_service import (
    add_device,
    delete_device_by_id,
    find_device_by_id,
    get_all_devices,
    update_device,
)

connected_clients: list[WebSocket] = []

router = APIRouter(prefix="/api/v1/devices", tags=["Devices"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_device_entry(
        db_session: DBSessionDep,
        device_request: DeviceRequestModel
) -> None:
    """Handles a request to add a new device entry to the database."""
    await add_device(db_session, device_request)


@router.get("/")
async def get_devices(
        db_session: DBSessionDep,
        device_type: str | None = None,
        status: str | None = None
) -> GetDevicesResponseModel:
    """
    Retrieves a list of devices based on optional device type and status filters.
    """
    query_filters = {}
    if device_type:
        query_filters["device_type"] = device_type
    if status:
        query_filters["status"] = status

    found_devices = await get_all_devices(db_session, query_filters)
    device_list = [DeviceGetModel(**device.__dict__) for device in found_devices]
    return GetDevicesResponseModel(devices=device_list)

@router.get("/{device_id}")
async def get_device(
        db_session: DBSessionDep,
        device_id: int
) -> GetDeviceResponseModel | list:
    """
    Handles the retrieval of device details based on the provided device ID. This
    function interacts with the database to find the corresponding device record
    and returns the device details in a structured format. If the device is not
    found, an empty list is returned.

    :param db_session: Database session dependency instance used to query the
        database.
    :type db_session: DBSessionDep

    :param device_id: Unique identifier for the device to be retrieved.
    :type device_id: int

    :return: An instance of GetDeviceResponseModel containing the device details
        if found, otherwise an empty list.
    :rtype: GetDeviceResponseModel | list
    """
    device = await find_device_by_id(db_session, device_id)
    if device:
        return GetDeviceResponseModel(device=DeviceGetModel(**device.__dict__))
    return []

@router.put("/{device_id}")
async def put_device(
        db_session: DBSessionDep,
        device_id: int,
        device_request: PutDeviceRequestModel
):
    """
    Handles HTTP PUT requests to update a device's information using its unique identifier.
    This function retrieves the device by its ID, and if it exists, updates its attributes
    based on the provided input data in the request body. Returns an updated device model
    on success or an HTTP 400 response if the device cannot be found.

    :param db_session: An object representing the database session dependency for executing
        queries and managing database operations.
    :type db_session: DBSessionDep
    :param device_id: The unique integer identifier of the device to be updated.
    :type device_id: int
    :param device_request: An instance of a request model containing new data to update
        the device's attributes.
    :type device_request: DeviceRequestModel
    :return: Returns an instance of PutDeviceResponseModel containing the updated
        device data if the operation is successful. Otherwise, returns an HTTP 400 response.
    :rtype: PutDeviceResponseModel or fastapi.Response
    """
    device = await find_device_by_id(db_session, device_id)
    if device:
        await update_device(db_session, device, device_request)
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{device_id}")
async def delete_device(
        db_session: DBSessionDep,
        device_id: int,
):
    """
    Deletes a device based on the provided device ID. The function attempts to find an existing
    device with the given ID in the database session. If a matching device is found, it deletes
    the device and returns a successful response. If no matching device is found, it returns
    a response indicating a bad request.

    :param db_session: Database session dependency, used for accessing and modifying the database.
    :type db_session: DBSessionDep
    :param device_id: The unique identifier of the device to be deleted.
    :type device_id: int
    :return: A response indicating the outcome of the operation. If the device is deleted
        successfully, returns a 200 OK response. Otherwise, returns a 400 Bad Request response.
    :rtype: Response
    """
    device = await find_device_by_id(db_session, device_id)
    if device:
        await delete_device_by_id(db_session, device)
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/{device_id}/command")
async def send_command(db_session: DBSessionDep, device_id:int, command_request: CommandRequestModel):
    device = await find_device_by_id(db_session, device_id)
    if device:
        match command_request.command:
            case "reboot":

                logger.info("Simulating reboot...")
                # Add a delay (e.g., 5 seconds) before continuing:
                await asyncio.sleep(5)
                logger.info("Reboot simulation complete.")
            case _:
                return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.websocket("/ws/devices")
async def websocket_endpoint(websocket: WebSocket):
    await connect_websocket(websocket)
    await handle_websocket_messages(websocket)

