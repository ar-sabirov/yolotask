from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    resource_url: str = Field("https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast", env='RESOURCE_URL')
    db_url: str = Field("redis://default:123@localhost:6379/0")
    max_workers: Optional[int] = None


settings: Settings = Settings()
