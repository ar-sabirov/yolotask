from pydantic import BaseSettings


class Settings(BaseSettings):
    resource_url: str = "https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast"
    db_url: str = "redis://default:123@localhost:6379/0"


settings = Settings()
