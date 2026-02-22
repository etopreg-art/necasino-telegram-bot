```python
import logging
from handlers.casino_handler import CasinoHandler

logger = logging.getLogger(__name__)

class MessageHandler:
"""
Основной обработчик сообщений от пользователей
"""

def __init__(self, telegram_api):
self.telegram_api = telegram_api
self.casino_handler = CasinoHandler(telegram_api)

def handle_update(self, update):
"""
Обработка входящих обновлений от Telegram
"""
try:
# Обработка обычных сообщений
if 'message' in update:
return self.handle_message(update['message'])

# Обработка callback запросов (нажатие на кнопки)
elif 'callback_query' in update:
return self.handle_callback_query(update['callback_query'])

# Обработка результатов игр казино
elif 'dice' in update.get('message', {}):
return self.casino_handler.handle_dice_result(update['message'])

return True

except Exception as e:
logger.error(f"Ошибка обработки обновления: {str(e)}")
return False

def handle_message(self, message):
"""
Обработка текстовых сообщений
"""
try:
chat_id = message['chat']['id']
text = message.get('text', '')
user_name = message.get('from', {}).get('first_name', 'Пользователь')

logger.info(f"Сообщение от {user_name} (ID: {chat_id}): {text}")

# Команда /start
if text == '/start':
return self.send_welcome_message(chat_id, user_name)

# Команда /help
elif text == '/help':
return self.send_help_message(chat_id)

# Команда /casino или /games
elif text in ['/casino', '/games
