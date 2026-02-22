```python
import asyncio
import logging
import sqlite3
import random
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8319790015:AAE1ahJe4htXLCO0L3yXUJ9IwVx5PgAIFNU"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ID группы NEC_Loyalty_Token
GROUP_ID = "@NEC_Loyalty_Token"

# Состояния для FSM
class UserStates(StatesGroup):
    waiting_deposit_amount = State()
    waiting_withdraw_amount = State()
    waiting_support_message = State()
    waiting_language_selection = State()

# Тексты интерфейса на разных языках
TEXTS = {
    'en': {
        'welcome': f"🎰 Welcome to NE Casino!\n\n💰 You've received 500 ₹ bonus for joining our casino!\n\nJoin our community: {GROUP_ID}\nMembers: 9,247",
        'balance': "💰 Your balance: {} ₹",
        'insufficient_funds': "❌ Insufficient funds! Your balance: {} ₹",
        'game_won': "🎉 Congratulations! You won {} ₹!",
        'game_lost': "😔 You lost {} ₹. Better luck next time!",
        'main_menu': "🎰 NE Casino - Main Menu",
        'games_menu': "🎮 Choose a game:",
        'settings_menu': "⚙️ Settings:",
        'support_menu': "📞 Support:\nOur administrators will help you with any questions.",
        'profile_info': "👤 Profile Information:\n💰 Balance: {} ₹\n🔗 Referral link: {}\n👥 Referrals: {}",
        'referral_reward': "🎁 Referral bonus! You received 100 ₹ for inviting a friend!",
        'language_selected': "✅ Language set to English",
        'deposit_prompt': "💳 Enter deposit amount in ₹:",
        'withdraw_prompt': "💸 Enter withdrawal amount in ₹:",
        'support_prompt': "📝 Describe your issue:",
        'deposit_success': "✅ Successfully deposited {} ₹!",
        'withdraw_success': "✅ Withdrawal request for {} ₹ submitted!",
        'support_sent': "✅ Your message has been sent to support!",
        'min_bet': "⚠️ Minimum bet: 10 ₹",
        'max_bet': "⚠️ Maximum bet: 1000 ₹",
        'join_group': f"❌ Please join our group first: {GROUP_ID}",
    },
    'ru': {
        'welcome': f"🎰 Добро пожаловать в NE Casino!\n\n💰 Вы получили бонус 500 ₹ за присоединение к казино!\n\nВступайте в наше сообщество: {GROUP_ID}\nУчастников: 9,247",
        'balance': "💰 Ваш баланс: {} ₹",
        'insufficient_funds': "❌ Недостаточно средств! Ваш баланс: {} ₹",
        'game_won': "🎉 Поздравляем! Вы выиграли {} ₹!",
        'game_lost': "😔 Вы проиграли {} ₹. Удачи в следующий раз!",
        'main_menu': "🎰 NE Casino - Главное меню",
        'games_menu': "🎮 Выберите игру:",
        'settings_menu': "⚙️ Настройки:",
        'support_menu': "📞 Поддержка:\nНаши администраторы помогут вам с любыми вопросами.",
        'profile_info': "👤 Информация о профиле:\n💰 Баланс: {} ₹\n🔗 Реферальная ссылка: {}\n👥 Рефералов: {}",
        'referral_reward': "🎁 Реферальный бонус! Вы получили 100 ₹ за приглашение друга!",
        'language_selected': "✅ Язык установлен на русский",
        'deposit_prompt': "💳 Введите сумму депозита в ₹:",
        'withdraw_prompt': "💸 Введите сумму для вывода в ₹:",
        'support_prompt': "📝 Опишите вашу проблему:",
        'deposit_success': "✅ Депозит {} ₹ успешно зачислен!",
        'withdraw_success': "✅ Заявка на вывод {} ₹ отправлена!",
        'support_sent': "✅ Ваше сообщение отправлено в поддержку!",
        'min_bet': "⚠️ Минимальная ставка: 10 ₹",
        'max_bet': "⚠️ Максимальная ставка: 1000 ₹",
        'join_group': f"❌ Пожалуйста, сначала вступите в нашу группу: {GROUP_ID}",
    },
    'hi': {
        'welcome': f"🎰 NE Casino में आपका स्वागत है!\n\n💰 कैसीनो में शामिल होने के लिए आपको 500 ₹ बोनस मिला!\n\nहमारे समुदाय में शामिल हों: {GROUP_ID}\nसदस्य: 9,247",
        'balance': "💰 आपका बैलेंस: {} ₹",
        'insufficient_funds': "❌ अपर्याप्त धन! आपका बैलेंस: {} ₹",
        'game_won': "🎉 बधाई हो! आपने {} ₹ जीते हैं!",
        'game_lost': "😔 आपने {} ₹ खो दिए। अगली बार भाग्य आजमाएं!",
        'main_menu': "🎰 NE Casino - मुख्य मेनू",
        'games_menu': "🎮 गेम चुनें:",
        'settings_menu': "⚙️ सेटिंग्स:",
        'support_menu': "📞 सहायता:\nहमारे प्रशासक किसी भी प्रश्न में आपकी सहायता करेंगे।",
        'profile_info': "👤 प्रोफाइल जानकारी:\n💰 बैलेंस: {} ₹\n🔗 रेफरल लिंक: {}\n👥 रेफरल: {}",
        'referral_reward': "🎁 रेफरल बोनस! दोस्त को आमंत्रित
