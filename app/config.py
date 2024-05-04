from pydantic import BaseSettings


class Settings(BaseSettings):
    account_name: str = "Nutanixdev"
    currencies: str = "USD,EUR,GBP"

    class Config:
        env_file = ".env"