from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "🎰 Добро пожаловать в NeCasino Support!\n\n"
        "Я помогу вам с вопросами по казино.\n"
        "Напишите ваш вопрос или выберите команду."
    )

def register_start_handlers(dp):
    dp.include_router(router)
