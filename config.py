import os
from dotenv import load_dotenv

ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.env"))
load_dotenv(dotenv_path=ENV_FILE_PATH)

print(os.getenv('API_ID'), type(os.getenv('API_ID')))

class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    GROUP_NAME = os.getenv("GROUP_NAME")
    bot_token = os.getenv("bot_token")
