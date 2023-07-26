import re
import datetime
import phonenumbers
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from phonenumbers.phonenumberutil import NumberParseException

from config import bot
from looping import pg
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class IsPhone(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        try:
            my_string_number = "+" + message.text
            my_number = phonenumbers.parse(my_string_number)
            if phonenumbers.is_valid_number(my_number) is True:
                return True
            else:
                await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)
        except NumberParseException:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsTitle(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if len(message.text) <= 100:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.lengthTitle)


class IsLegalAddress(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if len(message.text) <= 100:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.lengthLegalAddress)


class IsInn(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        inn = message.text
        pattern = r"^[0-9]{9}$"
        if re.match(pattern, inn) is not None:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsPinfl(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        inn = message.text
        pattern = r"^[0-9]{14}$"
        if re.match(pattern, inn) is not None:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsPaymentAccount(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        inn = message.text
        pattern = r"^[0-9]{20}$"
        if re.match(pattern, inn) is not None:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsBank(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if len(message.text) <= 100:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsMfo(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        inn = message.text
        pattern = r"^[0-9]{5}$"
        if re.match(pattern, inn) is not None:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsFio(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if len(message.text) <= 100:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsNumber(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if message.text.isnumeric() is True and len(message.text) <= 20:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsMinPayment(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if message.text.isnumeric() is True and len(message.text) <= 20:
            if int(message.text) >= Txt.commission.min_payment:
                return True
            else:
                await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.minPayment)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsDate(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        try:
            datetime.datetime.strptime(message.text, "%d.%m.%Y")
            return True
        except (TypeError, ValueError):
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsCardNumber(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        if message.text.isnumeric() is True and len(message.text) == 16:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsCardDate(BoundFilter):
    async def check(self, message: types.Message):
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        try:
            numbers = message.text.split('/')
            numbers = [int(i) for i in numbers]
            year = datetime.datetime.now().year
            if 0 < numbers[0] <= 12 and numbers[1] >= year - 2000:
                return True
            else:
                await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)
        except (TypeError, ValueError):
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)

