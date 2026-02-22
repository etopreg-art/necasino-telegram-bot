import os
import asyncio
from bot import main as bot_main
from fastapi import FastAPI
import uvicorn
from threading import Thread

# Создаем FastAPI приложение
app = FastAPI()

@app.get("/")
def read_root():
    """Главная страница API"""
    return {"status": "Bot is running"}

@app.get("/health")
def health_check():
    """Проверка состояния бота"""
    return {"status": "healthy"}

def run_bot():
    """Запускает Telegram бота в отдельном потоке"""
    asyncio.run(bot_main())

if __name__ == "__main__":
    # Запускаем бот в отдельном потоке
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем FastAPI сервер для Heroku/Railway
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
