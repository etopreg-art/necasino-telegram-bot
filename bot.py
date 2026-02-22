import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.getenv('PORT', 8000))

# Проверяем наличие токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Создаем клавиатуру
    keyboard = [
        [InlineKeyboardButton("📋 Помощь", callback_data='help')],
        [InlineKeyboardButton("ℹ️ О боте", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🤖 Привет, {user.first_name}!

Добро пожаловать в наш бот!
Используйте кнопки ниже для навигации.

Доступные команды:
/start - Запуск бота
/help - Помощь
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
📋 Помощь по использованию бота:

/start - Запуск бота
/help - Показать это сообщение

🔹 Просто напишите сообщение, и бот ответит вам!
    """
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    # Простая логика ответов
    if "привет" in user_message.lower():
        response = f"Привет, {user_name}! 👋"
    elif "как дела" in user_message.lower():
        response = "У меня всё отлично! А у вас? 😊"
    elif "спасибо" in user_message.lower():
        response = "Пожалуйста! Рад помочь! 🤗"
    else:
        response = f"Вы написали: {user_message}\nСпасибо за сообщение, {user_name}!"
    
    await update.message.reply_text(response)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        help_text = """
📋 Помощь по использованию бота:

🔹 Отправьте любое сообщение
🔹 Используйте команды /start, /help
🔹 Нажимайте на кнопки для навигации
        """
        await query.edit_message_text(help_text)
        
    elif query.data == 'about':
        about_text = """
ℹ️ О боте:

🤖 Простой Telegram бот
⚡ Работает на Python
🚀 Развернут на Render

Версия: 1.0
        """
        await query.edit_message_text(about_text)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")
    
    # Если есть update, отправляем сообщение об ошибке пользователю
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Произошла ошибка. Попробуйте позже."
        )

def main() -> None:
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота с webhook для Render
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_URL', 'your-app-name.onrender.com')}/{BOT_TOKEN}",
        url_path=BOT_TOKEN
    )

if __name__ == '__main__':
    main()
