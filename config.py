import os
from dotenv import load_dotenv

ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.env"))
load_dotenv(dotenv_path=ENV_FILE_PATH)

DEFAULT_SESSIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "telegram_service/sqlite_sessions"))
DEFAULT_SESSION_NAME = "developer.session"


class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    GROUP_NAME = os.getenv("GROUP_NAME")
    PHOTOS_ROOT = os.getenv("PHOTOS_ROOT")
    SESSION_PATH = os.getenv("SESSION_PATH", os.path.join(DEFAULT_SESSIONS_DIR, DEFAULT_SESSION_NAME))
    # TODO develop feature with several database controllers. Find a way how to flexible specify selected controller
    DB_CONTROLLER = "MongoController"
    MONGO_URI = "mongodb://localhost:27017/"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"