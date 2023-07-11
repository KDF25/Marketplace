from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, BotBlocked

from config import bot, moderation_chat_id
from filters.admin import IsAdmin
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi, pg
from model.moderation import ModerationModel
from text.blogger.formPlatform import FormPlatform
from text.fuction.function import TextFunc
from text.group.formModeration import FormModerationGroup
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class OnBanPlatform:

    async def start(self, message: types.Message):
        if len(str(message.text)) >= 5:
            await self._platform(message=message)
        else:
            Lang = Txt.language["rus"]
            await bot.send_message(text=Lang.alert.group.lenPlatform, chat_id=moderation_chat_id)

    async def _platform(self, message: types.Message):
        params = {"keyword": message.text}
        status, channels = await fastapi.get_platform_for_group(params=params)
        Lang = Txt.language["rus"]
        if status == 200 and len(channels) != 0:
            await self._get_all_channels(channels=channels)
        elif status == 200 and len(channels) == 0:
            await bot.send_message(text=Lang.alert.group.nonPlatform, chat_id=moderation_chat_id)
        else:
            await bot.send_message(text=Lang.alert.common.error, chat_id=moderation_chat_id)

    async def _get_all_channels(self, channels: list):
        for channel in channels:
            if channel.get("status") == "active":
                await self._ban(channel=channel)
            elif channel.get("status") == "banned":
                await self._unban(channel=channel)

    @staticmethod
    async def _ban(channel: dict):
        form = FormModerationGroup(data=channel, language="rus")
        inline = InlineGroupUser(language="rus", enter_id=channel.get("id"))
        await bot.send_message(chat_id=moderation_chat_id, text=await form.menu_ban(),
                               reply_markup=await inline.menu_ban(), disable_web_page_preview=True)

    @staticmethod
    async def _unban(channel: dict):
        form = FormModerationGroup(data=channel, language="rus")
        inline = InlineGroupUser(language="rus", enter_id=channel.get("id"))
        await bot.send_message(chat_id=moderation_chat_id, text=await form.menu_unban(),
                               reply_markup=await inline.menu_unban(), disable_web_page_preview=True)

