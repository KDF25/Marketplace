from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import *

from config import bot, moderation_chat_id
from filters.admin import IsAdmin
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi, pg
from model.all_orders import PostModel
from text.advertiser.formPostModeration import FormPostModeration
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class PostModerationGroup(StatesGroup):

    @staticmethod
    async def _prepare_group():
        lang = "rus"
        Lang: Model = Txt.language[lang]
        inline = InlineGroupUser(language=lang)
        return Lang, inline

    @staticmethod
    async def _error(call: types.CallbackQuery, Lang):
        await call.answer(text=Lang.alert.common.error, show_alert=True)

    @staticmethod
    async def _group(call: types.CallbackQuery, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=moderation_chat_id, text=Lang.group.post.solution,
                                        message_id=call.message.message_id)

    # menu moderation accept
    async def menu_favor_blogger(self, call: types.CallbackQuery, state: FSMContext):
        status, json = await self._moderation_blogger(call=call)
        await self._check_favor_blogger(call=call, status=status, json=json)

    @staticmethod
    async def _moderation_blogger(call: types.CallbackQuery):
        json = PostModel(blogger_area_id=int(call.data.split("_")[1]))
        status, json = await fastapi.favor_blogger(json=json)
        return status, json

    async def _check_favor_blogger(self, call: types.CallbackQuery, status: int, json: dict):
        Lang, inline = await self._prepare_group()
        if status == 200:
            status, json = await self._project(call)
            await self._send_favor_blogger(call=call, Lang=Lang, json=json)
        else:
            await self._error(call=call, Lang=Lang)

    async def _send_favor_blogger(self, call: types.CallbackQuery, json: dict , Lang):
        await self._group(call=call, Lang=Lang)
        await self._user_blogger_1(json=json)
        await self._user_advertiser_1(json=json)

    @staticmethod
    async def _project(call):
        params = PostModel(blogger_area_id=int(call.data.split("_")[1]))
        status, json = await fastapi.project_moderation(params=params)
        return status, json

    @staticmethod
    async def _user_blogger_1(json: dict):
        users = await pg.select_users(client_id=json.get("blogger_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormPostModeration(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_favor_blogger_blogger(),
                                       disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    @staticmethod
    async def _user_advertiser_1(json: dict):
        users = await pg.select_users(client_id=json.get("advertiser_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormPostModeration(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_favor_blogger_advertiser(),
                                       disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    # menu moderation accept
    async def menu_favor_advertiser(self, call: types.CallbackQuery, state: FSMContext):
        status, json = await self._moderation_advertiser(call=call)
        await self._check_favor_advertiser(call=call, status=status, json=json)

    @staticmethod
    async def _moderation_advertiser(call: types.CallbackQuery):
        json = PostModel(blogger_area_id=int(call.data.split("_")[1]))
        status, json = await fastapi.favor_advertiser(json=json)
        return status, json

    async def _check_favor_advertiser(self, call: types.CallbackQuery, status: int, json: dict):
        Lang, inline = await self._prepare_group()
        if status == 200:
            status, json = await self._project(call)
            await self._send_favor_advertiser(call=call, Lang=Lang, json=json)
        else:
            await self._error(call=call, Lang=Lang)

    async def _send_favor_advertiser(self, call: types.CallbackQuery, json: dict , Lang):
        await self._group(call=call, Lang=Lang)
        await self._user_blogger_2(json=json)
        await self._user_advertiser_2(json=json)


    @staticmethod
    async def _user_blogger_2(json: dict):
        users = await pg.select_users(client_id=json.get("blogger_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormPostModeration(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_favor_advertiser_blogger(),
                                       disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    @staticmethod
    async def _user_advertiser_2(json: dict):
        users = await pg.select_users(client_id=json.get("advertiser_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormPostModeration(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_favor_advertiser_advertiser(),
                                       disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    def register_handlers_moderation(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_favor_blogger, IsAdmin(),
                                           lambda x: x.data.startswith("FavorPostBlogger"),                             state="*")
        dp.register_callback_query_handler(self.menu_favor_advertiser, IsAdmin(),
                                           lambda x: x.data.startswith("FavorPostAdvertiser"),                          state="*")



