from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class InlineRegistration():
    def __init__(self, language: str):
        self.__markup = None
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_forgot_password(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.forgotPassword, callback_data="forgotPassword")
        markup.add(b1, self.__back)
        return markup

    async def menu_agreement(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.registration.agree, callback_data="agree")
        markup.add(b1)
        return markup

    async def menu_login(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.registration.have_account, callback_data="haveAccount")
        markup.add(b1, self.__back)
        return markup

    async def menu_code(self, second: int):
        markup = InlineKeyboardMarkup(row_width=1)
        text = f"{self.__Lang.buttons.registration.code} - {second}"
        b1 = InlineKeyboardButton(text=text, callback_data="void")
        markup.add(b1, self.__back)
        return markup

    async def menu_resend(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.registration.resend, callback_data="resendCode")
        markup.add(b1, self.__back)
        return markup

