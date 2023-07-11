from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text.language.main import Text_main

Txt = Text_main()


class InlinePersonalData():

    def __init__(self, language: str):
        self.__language = language
        self.__Lang = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")
        self.__confirm = InlineKeyboardButton(text=self.__Lang.buttons.common.confirm, callback_data="back")
        self.__accept = InlineKeyboardButton(text=self.__Lang.buttons.common.accept, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_first_data(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.accept, callback_data="confirm")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.changeData, callback_data="changeData")
        markup.add(b1, b2, self.__back)
        return markup

    async def menu_personal_data(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.accept, callback_data="confirm")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.changeData, callback_data="changeData")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.newData, callback_data="newData")
        markup.add(b1, b2, b3)
        return markup

    async def menu_logout(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.logout, callback_data="logout")
        markup.add(b1, self.__back)
        return markup

    async def menu_add_data(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.addData, callback_data="addData")
        markup.add(b1)
        return markup

    async def menu_employment(self, back=False):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.entity, callback_data="entity")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.individual, callback_data="individual")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.selfEmployedCard, callback_data="selfEmployedCard")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.selfEmployedAccount, callback_data="selfEmployedAccount")
        markup.add(b1, b2, b3, b4)
        if back is True:
            markup.add(self.__back)
        return markup

    async def menu_change_entity(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.titleFirm, callback_data="title")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.legalAddress, callback_data="legalAddress")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.inn, callback_data="inn")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.paymentAccount, callback_data="paymentAccount")
        b5 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.bank, callback_data="bank")
        b6 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.mfo, callback_data="mfo")
        b7 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.phone, callback_data="phone")
        markup.add(b1, b2, b3, b4, b5, b6, b7, self.__confirm)
        return markup

    async def menu_change_individual(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.titleIndividual, callback_data="title")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.legalAddress, callback_data="legalAddress")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.pinfl, callback_data="pinfl")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.paymentAccount, callback_data="paymentAccount")
        b5 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.bank, callback_data="bank")
        b6 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.mfo, callback_data="mfo")
        b7 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.phone, callback_data="phone")
        markup.add(b1, b2, b3, b4, b5, b6, b7, self.__confirm)
        return markup

    async def menu_change_self_employed_card(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.fioCard, callback_data="fio")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.number, callback_data="number")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.date, callback_data="date")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.pinfl, callback_data="pinfl")
        b5 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.transitAccount, callback_data="paymentAccount")
        b6 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.bank, callback_data="bank")
        b7 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.mfo, callback_data="mfo")
        b8 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.phone, callback_data="phone")
        b9 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.cardNumber, callback_data="cardNumber")
        b10 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.cardDate, callback_data="cardDate")
        markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, self.__confirm)
        return markup

    async def menu_change_self_employed_account(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.fio, callback_data="fio")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.number, callback_data="number")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.date, callback_data="date")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.pinfl, callback_data="pinfl")
        b5 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.paymentAccount, callback_data="paymentAccount")
        b6 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.bank, callback_data="bank")
        b7 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.mfo, callback_data="mfo")
        b8 = InlineKeyboardButton(text=self.__Lang.buttons.personalData.phone, callback_data="phone")
        markup.add(b1, b2, b3, b4, b5, b6, b7, b8, self.__confirm)
        return markup

    async def menu_confirm(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.accept, callback_data="confirm")
        markup.add(b1, self.__back)
        return markup


