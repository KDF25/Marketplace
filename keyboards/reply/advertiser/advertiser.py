from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class ReplyAdvertiser:
    def __init__(self, language: str):
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__main_menu = KeyboardButton(text=self.__Lang.buttons.common.menu)

    async def main_menu(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(self.__main_menu)
        return markup

    async def main_campaign(self, login: str, password: [int, str]):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.backOrder, web_app=WebAppInfo(url=await self._web_app(login, password)))
        markup.add(b1, self.__main_menu)
        return markup

    async def menu_accept(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.accept)
        markup.add(b1, self.__main_menu)
        return markup

    async def menu_basket(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.basket)
        markup.add(b1, self.__main_menu)
        return markup

    async def menu_task(self, login: str, password: [int, str]):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.task)
        b2 = KeyboardButton(text=self.__Lang.buttons.common.backOrder, web_app=WebAppInfo(url=await self._web_app(login, password)))
        markup.add(b1, b2, self.__main_menu)
        return markup

    async def _web_app(self, login: str, password: str, new_order: bool = False) -> str:
        return f'https://laappetit.uz?login={login}&password={password}&new_order={new_order}&language={self.__language}'


