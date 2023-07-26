from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class InlineWalletUser():

    def __init__(self, language: str):
        self.__markup = None
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_wallet(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.balance, callback_data="balance")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.withdraw, callback_data="withdraw")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.history, callback_data="history")
        markup.add(b1, b2, b3)
        return markup

    async def menu_payment_form_order(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.balance, callback_data="balance")
        markup.add(b1, self.__back)
        return markup

    async def menu_employment(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.entity, callback_data="entity")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.individual, callback_data="individual")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.selfEmployed2, callback_data="selfEmployed")
        markup.add(b1, b2, b3, self.__back)
        return markup

    async def menu_employment2(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.entity, callback_data="entity")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.individual, callback_data="individual")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.selfEmployedAccount, callback_data="selfEmployedAccount")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.selfEmployedCard, callback_data="selfEmployedCard")
        markup.add(b1, b2, b3, b4, self.__back)
        return markup

    async def menu_self_employed(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.emp, callback_data="emp")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.payme, callback_data="payme")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.click, callback_data="click")
        markup.add(b1).add(b2, b3).add(self.__back)
        return markup

    async def menu_payment(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.payment, callback_data="payment")
        markup.add(b1, self.__back)
        return markup

    async def menu_history(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.moreHistory, callback_data="moreHistory")
        markup.add(b1)
        return markup

