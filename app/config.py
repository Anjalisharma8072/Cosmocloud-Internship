import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI","")
    DATABASE_NAME: str = "student_db"

settings = Settings()