from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from models.common import PyObjectId, SailBaseModel
from pydantic import Field, StrictStr


class UserAccountState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class SocialMedia(Enum):
    TIKTOK = "TIKTOK"
    FACEBOOK = "FACEBOOK"
    TWITTER = "TWITTER"
    LINKEDIN = "LINKEDIN"
    INSTAGRAM = "INSTAGRAM"
    YOUTUBE = "YOUTUBE"
    PINTEREST = "PINTEREST"


class User_Base(SailBaseModel):
    name: StrictStr = Field(...)
    email: StrictStr = Field(...)
    avatar: Optional[StrictStr] = Field(default=None)


class User_Db(User_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    account_creation_time: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: StrictStr = Field(...)
    account_state: UserAccountState = Field(...)
    social_media: Dict[SocialMedia, str] = Field(default=[])


class UserInfo_Out(User_Base):
    id: PyObjectId = Field(alias="_id")


class RegisterUser_In(User_Base):
    password: str = Field(...)


class RegisterUser_Out(SailBaseModel):
    id: PyObjectId = Field(alias="_id")


class GetUsers_Out(User_Base):
    id: PyObjectId = Field(alias="_id")
    name: StrictStr = Field(...)
    email: StrictStr = Field(...)
    avatar: Optional[StrictStr] = Field(...)
    social_media: Dict[SocialMedia, str] = Field(default=[])


class GetMultipleUsers_Out(SailBaseModel):
    users: List[GetUsers_Out] = Field(...)


class AddSocialMedia_In(SailBaseModel):
    social_media: Dict[SocialMedia, str] = Field(...)
