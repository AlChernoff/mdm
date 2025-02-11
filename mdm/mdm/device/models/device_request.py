from typing import Optional

from pydantic import BaseModel, ConfigDict

from mdm.device.schemas.device import DeviceType, Status


class DeviceRequestModel(BaseModel):
    device_name: str
    device_type: DeviceType
    status: Status

class PutDeviceRequestModel(BaseModel):
    device_name: Optional[str] = None
    device_type: Optional[DeviceType] = None
    status: Optional[Status] = None

class DeviceGetModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    device_name: str
    device_type: DeviceType
    status: Status


class GetDevicesResponseModel(BaseModel):
    devices: list[DeviceGetModel]

class GetDeviceResponseModel(BaseModel):
    device: DeviceGetModel

class PutDeviceResponseModel(BaseModel):
    device: DeviceGetModel

class CommandRequestModel(BaseModel):
    command: str