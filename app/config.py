import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE=os.getenv("MYSQL_DATABASE")
    _cors_env = os.getenv("CORS_ORIGIN", "*")
    CORS_ORIGIN = _cors_env.split(",") if "," in _cors_env else [_cors_env]