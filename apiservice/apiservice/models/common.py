from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StrictStr


class PyObjectId(UUID):
    def __init__(self, value: Optional[str] = None, empty: bool = False):
        if empty:
            return super().__init__(str(UUID(int=0)))
        elif value is None:
            return super().__init__(str(uuid4()))
        else:
            return super().__init__(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        uuid_obj = UUID(str(v), version=4)
        return UUID(str(v), version=4)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SailBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class BasicObjectInfo(SailBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    name: StrictStr = Field(...)


class KeyVaultObject(BaseModel):
    name: StrictStr = Field(...)
    version: StrictStr = Field(...)
