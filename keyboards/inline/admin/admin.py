from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.language.main import Text_main

Txt = Text_main()


class InlineAdmin:

    @staticmethod
    async def menu_admin():
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text="Рассылка", callback_data="mail")
        b2 = InlineKeyboardButton(text="Статистика", callback_data="statistics")
        markup.add(b1, b2)
        return markup

    @staticmethod
    async def menu_period():
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text="День", callback_data="day")
        b2 = InlineKeyboardButton(text="Неделя", callback_data="week")
        b3 = InlineKeyboardButton(text="Месяц", callback_data="month")
        b4 = InlineKeyboardButton(text="⬅ Назад", callback_data="back")
        markup.add(b1, b2, b3).add(b4)
        return markup

    @staticmethod
    async def menu_send():
        markup = InlineKeyboardMarkup(row_width=1)
        b_yes = InlineKeyboardButton(text="✅ Да", callback_data="yes")
        b_cancel = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
        markup.add(b_yes, b_cancel)
        return markup

    @staticmethod
    async def menu_back():
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text="⬅ Назад", callback_data="back")
        markup.add(b)
        return markup
