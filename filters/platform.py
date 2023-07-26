import re
import urllib
from aiogram.dispatcher.filters import Text, BoundFilter
from config import bot
from aiogram import types
import typing

from looping import pg
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class IsTelegram(BoundFilter):
    async def check(self, message: types.Message):
        print("get")
        print(('Join Channel' in str(urllib.request.urlopen(message.text).read())))
        if ('Join Channel' in str(urllib.request.urlopen(message.text).read())) is True:
            print(('Join Channel' in str(urllib.request.urlopen(message.text).read())))
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.invalidUrl)



class IsTitle(BoundFilter):
    async def check(self, message: types.Message):

        if len(message.text) <= 20:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.lengthTitle)


class IsInstagram(BoundFilter):
    async def check(self, call: types.CallbackQuery):

        if int(call.data.split("_")[1]) != 3:
            return True
        else:
            lang = await pg.select_language(user_id=call.from_user.id)
            Lang: Model = Txt.language[lang]
            await call.answer(text=Lang.alert.blogger.instagram, show_alert=True)


class IsDescription(BoundFilter):
    async def check(self, message: types.Message):
        if len(message.text) <= 150:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.lengthDescription)


class IsPrice(BoundFilter):
    async def check(self, message: types.Message):
        price = message.text
        pattern = r"^[0-9]{,9}$"
        if re.match(pattern, price) is not None:
            if int(message.text) >= 10000:
                return True
            else:
                lang = await pg.select_language(user_id=message.from_user.id)
                Lang: Model = Txt.language[lang]
                await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.blogger.minPrice)
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.lengthPrice)



class LenSymbol(BoundFilter):
    async def check(self, message: types.Message):
        price = message.text
        pattern = r"^[0-9]{,5}$"
        if re.match(pattern, price) is not None:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)
