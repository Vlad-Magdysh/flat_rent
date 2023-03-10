import json
from telegram_service import TelegramService

ts = TelegramService()
print(json.dumps(ts.get_messages(min_message_id=77800), indent=4, default=str))
