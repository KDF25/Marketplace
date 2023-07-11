from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text.language.main import Text_main

Txt = Text_main()


class InlineGroupUser():

    def __init__(self, language: str, enter_id: int = None):
        self.__language = language
        self.__enter_id = enter_id
        self.__Lang = Txt.language[language]

    async def menu_withdraw_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"withdrawBack")
        markup.add(back)
        return markup

    async def menu_withdraw(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.acceptWithdraw,
                                  callback_data=f"withdrawAccept_{self.__enter_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.wallet.rejectWithdraw,
                                  callback_data=f"withdrawReject_{self.__enter_id}")
        markup.add(b1, b2)
        return markup

    async def menu_moderation_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"moderationBack")
        markup.add(back)
        return markup

    async def menu_moderation(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.accept,
                                  callback_data=f"moderationAccept_{self.__enter_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.platform.reject,
                                  callback_data=f"moderationReject_{self.__enter_id}")
        markup.add(b1, b2)
        return markup

    async def menu_ban(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.banPlatform.ban, callback_data=f"banPlatform_{self.__enter_id}")
        markup.add(b1)
        return markup

    async def menu_unban(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.banPlatform.unban, callback_data=f"unbanPlatform_{self.__enter_id}")
        markup.add(b1)
        return markup

    async def menu_ban_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"banBack")
        markup.add(back)
        return markup
