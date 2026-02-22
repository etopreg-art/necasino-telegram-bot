import json
from utils.telegram_api import send_message

class CasinoHandler:
    def __init__(self):
        # База знаний для ответов
        self.responses = {
            'deposit': self.help_deposit,
            'withdraw': self.help_withdraw, 
            'bonus': self.help_bonus,
            'games': self.help_games,
            'technical': self.help_technical,
            'rules': self.help_rules
        }
    
    def handle_support_request(self, chat_id, message_text):
        """Обработка запроса поддержки"""
        text = message_text.lower()
        
        # Определяем тип вопроса
        if any(word in text for word in ['депозит', 'пополнить', 'внести']):
            return self.help_deposit(chat_id)
        elif any(word in text for word in ['вывод', 'вывести', 'снять']):
            return self.help_withdraw(chat_id)
        elif any(word in text for word in ['бонус', 'промокод', 'фриспин']):
            return self.help_bonus(chat_id)
        elif any(word in text for word in ['игра', 'слоты', 'правила']):
            return self.help_games(chat_id)
        elif any(word in text for word in ['не работает', 'ошибка', 'баг']):
            return self.help_technical(chat_id)
        else:
            return self.general_help(chat_id)
    
    def help_deposit(self, chat_id):
        """Помощь с депозитом"""
        message = """💰 ПОПОЛНЕНИЕ СЧЕТА

🔸 Минимальный депозит: 100₽
🔸 Без комиссии от казино
🔸 Зачисление моментальное

💳 СПОСОБЫ ОПЛАТЫ:
• Карта Visa/MasterCard
• СБП (Система Быстрых Платежей)  
• Qiwi, ЮMoney
• Криптовалюта

❓ Проблемы с пополнением?
Пишите @support_casino"""
        
        return send_message(chat_id, message)
