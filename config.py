import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Database settings
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///casino_bot.db')

# Casino API settings (если есть)
CASINO_API_KEY = os.getenv('CASINO_API_KEY', '')
CASINO_API_URL = os.getenv('CASINO_API_URL', '')

# Admin settings
ADMIN_USER_IDS = [
    int(x) for x in os.getenv('ADMIN_USER_IDS', '').split(',') if x.strip()
]

# Bot settings
BOT_USERNAME = os.getenv('BOT_USERNAME', 'neonline_support_bot')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# Support settings
HUMAN_SUPPORT_USERNAME = '@Neonline_support'

# Rate limiting
MAX_MESSAGES_PER_MINUTE = int(os.getenv('MAX_MESSAGES_PER_MINUTE', '10'))

# Development mode
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Timezone
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Kolkata')
