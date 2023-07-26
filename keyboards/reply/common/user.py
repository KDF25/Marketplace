from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class ReplyUser:
    def __init__(self, language: str):
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__main_menu = KeyboardButton(text=self.__Lang.buttons.common.menu)

    async def start(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=False, row_width=2)
        b1 = KeyboardButton(text=self.__Lang.start.blogger)
        b2 = KeyboardButton(text=self.__Lang.start.advertiser)
        b3 = KeyboardButton(text=self.__Lang.start.language)
        markup.add(b1, b2, b3)
        return markup

    async def main_menu(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(self.__main_menu)
        return markup

    async def menu_start(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.start)
        markup.add(b1, self.__main_menu)
        return markup

    async def menu_skip(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.skip)
        markup.add(b1, self.__main_menu)
        return markup

    async def menu_next_time(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Lang.buttons.common.nextTime)
        markup.add(b1, self.__main_menu)
        return markup

    async def menu_blogger(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Lang.menu.blogger.platform)
        b2 = KeyboardButton(text=self.__Lang.menu.blogger.activeOrder)
        b3 = KeyboardButton(text=self.__Lang.menu.blogger.account)
        b4 = KeyboardButton(text=self.__Lang.menu.blogger.wallet)
        b5 = KeyboardButton(text=self.__Lang.menu.blogger.information)
        b6 = KeyboardButton(text=self.__Lang.menu.blogger.lang)
        b7 = KeyboardButton(text=self.__Lang.menu.blogger.change)
        markup.add(b1, b2, b3, b4, b5, b6).add(b7)
        return markup

    async def menu_advertiser(self, login: str, password: [int, str]):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Lang.menu.advertiser.formOrder, web_app=WebAppInfo(url=await self._web_app(login, password)))
        b2 = KeyboardButton(text=self.__Lang.menu.advertiser.activeOrder)
        b3 = KeyboardButton(text=self.__Lang.menu.advertiser.basket)
        b4 = KeyboardButton(text=self.__Lang.menu.advertiser.account)
        b5 = KeyboardButton(text=self.__Lang.menu.advertiser.wallet)
        b6 = KeyboardButton(text=self.__Lang.menu.advertiser.information)
        b7 = KeyboardButton(text=self.__Lang.menu.advertiser.lang)
        b8 = KeyboardButton(text=self.__Lang.menu.advertiser.change)
        markup.add(b1).add(b2, b3, b4, b5, b6, b7).add(b8)
        return markup

    async def _web_app(self, login: str, password: str, new_order: bool = True) -> str:
        return f'https://laappetit.uz?login={login}&password={password}&new_order={new_order}&language={self.__language}'

    async def information(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Lang.information.about_us)
        b2 = KeyboardButton(text=self.__Lang.information.how_to_use)
        b3 = KeyboardButton(text=self.__Lang.information.feedback)
        markup.add(b1, b2).add(b3).add(self.__main_menu)
        return markup

    async def personal_data(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b = KeyboardButton(text=self.__Lang.buttons.personalData.logoutAccount)
        markup.add(b, self.__main_menu)
        return markup

    async def setting(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        b1 = KeyboardButton(text=Txt.settings.rus)
        b2 = KeyboardButton(text=Txt.settings.uzb)
        # b3 = KeyboardButton(text=Txt.settings.eng)
        markup.add(b1, b2).add(self.__main_menu)
        return markup
