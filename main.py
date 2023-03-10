import datetime
import json
import os
from telethon.sync import TelegramClient
from config import Config
SESSIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "telegram_service/sqlite_sessions"))

SESSION_NAME = "developer.session"

client = TelegramClient(os.path.join(SESSIONS_DIR, SESSION_NAME), Config.API_ID, Config.API_HASH)
client.start()

# get the group by its name
entity = client.get_entity(Config.GROUP_NAME)
# make sure that the entity is a group chat
# if not isinstance(entity, PeerChat):
#     raise ValueError(f"{group_name} is not a group chat.")
date=datetime.datetime(2023, 3, 3, 14, 47, 32, tzinfo=datetime.timezone.utc)
# get the messages from the group
messages = client.get_messages(entity, limit=40, min_id=77810)

# write the messages to a text file
with open("publications.txt", 'w', encoding='utf-8') as f:
    for message in messages:
        print(json.dumps(message))
        if message.message:
            f.write(message.message + '\n')

client.disconnect()







