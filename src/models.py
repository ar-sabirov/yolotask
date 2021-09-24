from pydantic import BaseModel, Field


class RequestModel(BaseModel):
    # ellipsis (...) annotates required fields
    sdk_version: str = Field(..., alias="SDK Version")
    session_id: str = Field(..., alias="SessionId")
    platform: str = Field(..., alias="Platform")
    user_name: str = Field(..., alias="User name")
    country_code: str = Field(..., alias="Country code")
