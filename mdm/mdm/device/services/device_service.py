from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mdm.device.models.device_request import DeviceRequestModel, PutDeviceRequestModel
from mdm.device.schemas import Device
from mdm.device.services.websockets_service import notify_device_change
from mdm.logging_config import logger


async def  add_device(db_session: AsyncSession, device_request) -> None:
    try:
        async with db_session.begin():
            new_device = Device(device_name=device_request.device_name, device_type=device_request.device_type, status=device_request.status)
            db_session.add(new_device)
            await db_session.flush()
            await db_session.refresh(new_device)
            logger.info(f"Device '{device_request.device_name}' added successfully.")
            # Notify clients
            await notify_device_change(device_id=new_device.id, change_type="created")


    except Exception as e:
        logger.error(f"Failed to add device: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add device. Please try again later."
        )

async def get_all_devices(db_session: AsyncSession, filters: dict[str, str] | None) -> Sequence[Device] | None:
    query = select(Device)

    if filters:
        for field_name, value in filters.items():
            # Assuming exact matches on fields; adjust logic if needed (e.g., partial matching)
            query = query.where(getattr(Device, field_name) == value.lower())

    result = await db_session.execute(query)
    return result.scalars().all()

async def find_device_by_id(db_session: AsyncSession, device_id: int) -> Device | None:
    result = await db_session.execute(select(Device).where(Device.id == device_id))
    return result.scalars().first()



async def update_device(
        db_session: AsyncSession,
        device: Device,
        device_request: PutDeviceRequestModel
) -> Device:
    # Convert request to a dictionary, excluding any unset or special fields
    updated_fields = device_request.model_dump(exclude_unset=True) \
        if hasattr(device_request, 'dict') else dict(device_request)

    # Update only the fields that match attributes on the device
    for field_name, field_value in updated_fields.items():
        # Skip the device ID or any fields you do not want to modify
        if field_name != "id" and hasattr(device, field_name):
            setattr(device, field_name, field_value)

    await db_session.commit()

    return device

async def delete_device_by_id(db_session: AsyncSession, device: Device) -> None:
    try:
        await db_session.delete(device)
        await db_session.commit()
    except Exception as e:
        logger.error(f"Failed to delete device: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete device. Please try again later."
        )