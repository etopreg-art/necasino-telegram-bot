import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    """
    Конфигурация Flask приложения
    """
    # Основные настройки Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Настройки Telegram бота
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://yourdomain.com/webhook')
    
    # Настройки базы данных (при необходимости)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///casino_bot.db')
    
    # Настройки казино
    CASINO_GAMES = ['🎰', '🎲', '🏀', '⚽', '🎯', '🎳']
    WIN_MULTIPLIERS = {
        '🎰': 2.5,
        '🎲': 3.0,
        '🏀': 2.0,
        '⚽': 2.0,
        '🎯': 4.0,
        '🎳': 3.5
    }
