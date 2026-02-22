import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramAPI:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, chat_id, text, parse_mode="HTML", reply_markup=None):
        """Отправка сообщения в чат"""
        url = f"{self.base_url}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def edit_message(self, chat_id, message_id, text, parse_mode="HTML", reply_markup=None):
        """Редактирование сообщения"""
        url = f"{self.base_url}/editMessageText"
        
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error editing message: {e}")
            return None
    
    def delete_message(self, chat_id, message_id):
        """Удаление сообщения"""
        url = f"{self.base_url}/deleteMessage"
        
        data = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting message: {e}")
            return None

# Глобальная функция для быстрого использования
def send_message(chat_id, text, parse_mode="HTML", reply_markup=None):
    """Быстрая отправка сообщения (нужен токен из конфига)"""
    # Токен будет браться из config.py
    from config import BOT_TOKEN
    api = TelegramAPI(BOT_TOKEN)
    return api.send_message(chat_id, text, parse_mode, reply_markup)
