from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class ReplyStart:
    def __init__(self, language: str = 'rus'):
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__main_menu = KeyboardButton(text=self.__Lang.buttons.common.menu)

    async def start(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Lang.start.blogger)
        b2 = KeyboardButton(text=self.__Lang.start.advertiser)
        b3 = KeyboardButton(text=self.__Lang.start.language)
        markup.add(b1, b2, b3)
        return markup

    async def setting(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        b1 = KeyboardButton(text=Txt.settings.rus)
        b2 = KeyboardButton(text=Txt.settings.uzb)
        # b3 = KeyboardButton(text=Txt.settings.eng)
        markup.add(b1, b2).add(self.__main_menu)
        return markup
