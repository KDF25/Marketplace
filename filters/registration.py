from aiogram.dispatcher.filters import Text, BoundFilter
from config import bot
from aiogram import types
from looping import fastapi

from looping import pg
from text.language.main import Text_main

import re
Txt = Text_main()


class HaveAccount(BoundFilter):
    async def check(self, message: types.Message):
        return True


class IsEmail(BoundFilter):
    async def check(self, message: types.Message):
        email = message.text
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if re.match(pattern, email) is not None:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Text_lang = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.common.nonFormat)


class IsNew(BoundFilter):
    async def check(self, message: types.Message):
        email = message.text
        status, json = await fastapi.exist_user(email=email)
        if json.get("error") == "user does not exist":
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Text_lang = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.common.existUser)


class IsExist(BoundFilter):
    async def check(self, message: types.Message):
        email = message.text
        status, json = await fastapi.exist_user(email=email)
        if status == 200:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Text_lang = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.common.nonAccount)


class IsCode(BoundFilter):
    async def check(self, message: types.Message):
        return True


class IsPassword(BoundFilter):
    async def check(self, message: types.Message):
        password = message.text
        pattern = r"^[A-Za-z\d_@$!%*?&]{8,}$"
        if re.match(pattern, password) is not None:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Text_lang = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.common.nonFormat)

