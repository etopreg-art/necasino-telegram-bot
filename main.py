import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database import create_tables
from handlers.start_handler import register_start_handlers
from handlers.support_handler import register_support_handlers
from handlers.casino_handler import register_casino_handlers

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создание бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def on_startup():
    """Функция запуска бота"""
    logger.info("Создание таблиц базы данных...")
    create_tables()
    
    logger.info("Регистрация обработчиков...")
    register_start_handlers(dp)
    register_support_handlers(dp)
    register_casino_handlers(dp)
    
    logger.info("🚀 Neonline Support Bot запущен!")

async def on_shutdown():
    """Функция остановки бота"""
    logger.info("❌ Neonline Support Bot остановлен!")
    await bot.session.close()

async def main():
    """Основная функция запуска"""
    try:
        await on_startup()
        
        # Запуск polling
        await dp.start_polling(
            bot,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True
        )
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
