import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Parasite & Disease Classification API"
    MODEL_PATH: str = "app/models_weights/malaria_best.pth"
    CLASSES: list = ["Negative", "Positive"]
    
    class Config:
        env_file = ".env"

settings = Settings()