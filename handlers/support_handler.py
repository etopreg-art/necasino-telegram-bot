from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def support_message(message: Message):
    await message.answer(
        f"Получил ваше сообщение: {message.text}\n\n"
        "Наши операторы свяжутся с вами в ближайшее время!"
    )

def register_support_handlers(dp):
    dp.include_router(router)
