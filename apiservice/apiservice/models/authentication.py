from models.common import PyObjectId, SailBaseModel
from pydantic import Field, StrictStr


class LoginSuccess_Out(SailBaseModel):
    access_token: StrictStr
    token_type: StrictStr


class TokenData(SailBaseModel):
    id: PyObjectId = Field(alias="_id")
    exp: int = Field(...)
