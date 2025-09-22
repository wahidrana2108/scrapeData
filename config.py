import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_URI = os.getenv("DB_URI")

settings = Settings()
