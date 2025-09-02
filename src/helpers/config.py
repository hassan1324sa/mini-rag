from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    COHERE_API_KEY:str
    FILE_ALLOWED_EXTNSTIONS:list
    FILE_MAX_SIZE:int

    class Config:
        env_file=".env"
        env_file_encoding = "utf-8"



def getSettings():
    return Settings()