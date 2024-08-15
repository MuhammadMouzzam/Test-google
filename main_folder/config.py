from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    client_id : str
    client_secret : str
    class config:
        env_file = '.env'

settings = Settings()
