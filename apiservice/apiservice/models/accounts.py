from datetime import datetime
from enum import Enum
from typing import List, Optional

from models.common import PyObjectId, SailBaseModel
from pydantic import EmailStr, Field, StrictStr


class UserAccountState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class User_Base(SailBaseModel):
    name: StrictStr = Field(...)
    email: EmailStr = Field(...)
    avatar: Optional[StrictStr] = Field(default=None)


class User_Db(User_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    account_creation_time: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: StrictStr = Field(...)
    account_state: UserAccountState = Field(...)


class UserInfo_Out(User_Base):
    id: PyObjectId = Field(alias="_id")


class RegisterUser_In(User_Base):
    password: str = Field(...)


class RegisterUser_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetUsers_Out(User_Base):
    id: PyObjectId = Field(alias="_id")
    name: StrictStr = Field(...)
    email: EmailStr = Field(...)
    avatar: Optional[StrictStr] = Field(...)


class GetMultipleUsers_Out(SailBaseModel):
    users: List[GetUsers_Out] = Field(...)
