from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum, IntEnum
from typing import ForwardRef, List, Optional

class DepartmentEnum(str, Enum):
    Trading = "Trading"
    Development = "Development"
    
class DeviceTypeEnum(str, Enum):
    Workstation = "Workstation"
    Laptop = "Laptop"

class LockBase(BaseModel):
    computer_id: str
    user_id: str
    
class Lock(LockBase):
    id: str
    lock_time: datetime
    expire_time: datetime
    created_at: datetime
    updated_at: datetime
    computer_id: str
    user_id: str
    
class LockCreate(LockBase):
    pass
    
class UserBase(BaseModel):
    name: str
    samAccountName: str
    ou: str

class ComputerBase(BaseModel):
    name: str
    department: DepartmentEnum
    type: DeviceTypeEnum

    
class Computer(ComputerBase):
    id: str
    is_available: bool 
    created_at: datetime
    updated_at: datetime
    lock: Optional[Lock] = None
    user_id: Optional[str] = None
    # user: Optional['User'] = None
    model_config = ConfigDict(from_attributes=True)

    
class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    computers: List[Computer] = []
    lock: Optional[Lock] = None
    
    model_config = ConfigDict(from_attributes=True)
    
# Computer.update_forward_refs()

class UserCreate(UserBase):
    pass
    
class ComputerCreate(ComputerBase):
    pass


    
