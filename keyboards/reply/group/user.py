from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text.language.main import Text_main

Txt = Text_main()


class ReplyUser:
    def __init__(self):
        self.__Lang = Txt.language["rus"]

    @staticmethod
    async def menu_group():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=Txt.group.moderation)
        b2 = KeyboardButton(text=Txt.group.withdraw)
        b3 = KeyboardButton(text=Txt.group.banPlatform)
        markup.add(b1, b2, b3)
        return markup
