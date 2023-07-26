from aiogram.dispatcher.filters import Text, BoundFilter
from config import bot
from aiogram import types

from looping import pg
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class IsSearch(BoundFilter):
    async def check(self, message: types.Message):
        text = message.text
        if len(text) < 3:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.searchMin)
        elif len(text) > 10:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.lengthMax)
        else:
            return True


class IsPostLength(BoundFilter):
    async def check(self, message: types.Message):
        max_len = 1500
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        try:
            text = message.html_text
            if len(message.photo) != 0:
                if len(message.caption) <= max_len:
                    return True
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.lengthPost)
            elif message.video is not None:
                if len(message.caption) <= max_len:
                    return True
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.lengthPost)
            elif message.text is not None:
                if len(message.text) <= max_len:
                    return True
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.lengthPost)
        except TypeError:
            return True


class IsCommentLength(BoundFilter):
    async def check(self, message: types.Message):
        max_len = 100
        text = message.text
        if len(text) <= max_len:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.lengthComment)


class IsUrlButton(BoundFilter):
    async def check(self, message: types.Message):
        max_len = 3
        lang = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[lang]
        try:
            buttons = message.text
            buttons = [i.split("|") for i in buttons.split("\n")]
            unpack = []
            for group in buttons:
                unpack += group
            for button in unpack:
                text, url = button.split("-")
                url = url.replace(' ', '')
                if url.startswith("https://") is False:
                    # await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)
                    raise Exception
            else:
                if len(unpack) <= max_len:
                    return True
                else:
                    lang = await pg.select_language(user_id=message.from_user.id)
                    Lang: Model = Txt.language[lang]
                    await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.lengthButton)
        except Exception:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)


class IsPost(BoundFilter):
    async def check(self, message: types.Message):
        if str(message.text).startswith("https://") is True or str(message.text).startswith("http://") is True:
            return True
        else:
            lang = await pg.select_language(user_id=message.from_user.id)
            Lang: Model = Txt.language[lang]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)



