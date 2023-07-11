import re
import datetime
import phonenumbers
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from phonenumbers.phonenumberutil import NumberParseException

from config import bot
from looping import pg
from text.language.main import Text_main

Txt = Text_main()


class IsWithdraw(BoundFilter):
    async def check(self, message: types.Message):
        price = message.text
        pattern = r"^[0-9]{,9}$"
        if re.match(pattern, price) is not None:
            if int(message.text) >= Text_main.commission.min_payment:
                return True
            else:
                lang = await pg.select_language(user_id=message.from_user.id)
                Text_lang = Txt.language[lang]
                await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.common.minWithdraw)
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Text_lang = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.common.lengthPrice)