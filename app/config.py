from pydantic import BaseSettings


# pydantic will automatically understand lowercase and uppercase env variables
# it validates type checks
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
