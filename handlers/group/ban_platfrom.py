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
from text.fuction.function import TextFunc
from text.group.formModeration import FormModerationGroup
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class BanPlatformGroup(StatesGroup):

    # menu unban
    async def menu_unban(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuGroup:start")
        status, json = await self._moderation_unban(call=call)
        await self._check_unban(call=call, status=status, json=json)

    @staticmethod
    async def _moderation_unban(call: types.CallbackQuery):
        json = ModerationModel(area_id=int(call.data.split("_")[1]))
        status, json = await fastapi.unban_platform(json=json)
        return status, json

    @staticmethod
    async def _prepare_group():
        lang = "rus"
        Lang = Txt.language[lang]
        inline = InlineGroupUser(language=lang)
        return Lang, inline

    async def _check_unban(self, call: types.CallbackQuery, status: int, json: dict):
        Lang, inline = await self._prepare_group()
        if status == 200:
            await self._unban(call=call, Lang=Lang, json=json)
        else:
            await self._error(call=call, Lang=Lang)

    async def _unban(self, call: types.CallbackQuery, json: dict, Lang):
        await self._group_unban(call=call, Lang=Lang)
        await self._user_unban(json=json)

    @staticmethod
    async def _error(call: types.CallbackQuery, Lang):
        await call.answer(text=Lang.alert.common.error, show_alert=True)

    @staticmethod
    async def _group_unban(call: types.CallbackQuery, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=moderation_chat_id, text=Lang.group.moderation.group.unban,
                                        message_id=call.message.message_id, disable_web_page_preview=True)

    @staticmethod
    async def _user_unban(json: dict):
        users = await pg.select_users(client_id=json.get("client_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormModerationGroup(language=lang_user, url=json.get("url"), name=json.get("name"))
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_unban_platform(),
                                       disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    # menu moderation cancel
    async def menu_ban_cancel(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuGroup:start")
        Lang, inline = await self._prepare_group()
        await self._cancel(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _cancel(call: types.CallbackQuery, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            text = f"{call.message.html_text}\n\n{Lang.group.moderation.group.reason}\n\n#banId_{call.data.split('_')[1]}"
            await bot.edit_message_text(chat_id=moderation_chat_id, text=text, parse_mode="html",
                                        reply_markup=await inline.menu_ban_back(),
                                        message_id=call.message.message_id, disable_web_page_preview=True)

    # menu moderation cancel back
    async def menu_ban_back(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuGroup:start")
        area_id = await self._unpack_call(call=call)
        Lang, inline = await self._prepare_ban_back(area_id=area_id)
        await self._ban_back(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _unpack_call(call: types.CallbackQuery):
        entities = call.message.entities
        area_id = int(entities[-1].get_text(call.message.text).split('_')[1])
        return area_id

    @staticmethod
    async def _prepare_ban_back(area_id: int):
        lang = "rus"
        Lang = Txt.language[lang]
        inline = InlineGroupUser(language=lang, enter_id=area_id)
        return Lang, inline

    @staticmethod
    async def _ban_back(call: types.CallbackQuery, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            text = call.message.html_text.split(Lang.group.moderation.group.reason)[0]
            await bot.edit_message_text(chat_id=moderation_chat_id, text=text, message_id=call.message.message_id,
                                        disable_web_page_preview=True, reply_markup=await inline.menu_ban())

    # menu moderation reject
    async def menu_ban(self, message: types.Message):
        await self._answer(message=message)

    async def _answer(self, message: types.Message):
        try:
            area_id = await self._unpack_message(message=message)
            status, json = await self._ban_platform(area_id=area_id, message=message)
            await self._check_ban(message=message, status=status, json=json)
        except BaseException:
            Lang, inline = await self._prepare_group()
            await self._error_message(Lang=Lang)

    @staticmethod
    async def _unpack_message(message: types.Message):
        entities = message.reply_to_message.entities
        area_id = int(entities[-1].get_text(message.reply_to_message.text).split('_')[1])
        return area_id

    @staticmethod
    async def _ban_platform(area_id: int, message: types.Message):
        json = ModerationModel(area_id=area_id, reason=message.text)
        status, json = await fastapi.ban_platform(json=json)
        return status, json

    async def _check_ban(self, message: types.Message, status: int, json: dict):
        Lang, inline = await self._prepare_group()
        if status == 200:
            await self._ban(message=message, json=json, Lang=Lang)
        else:
            await self._error_message(Lang=Lang)

    @staticmethod
    async def _error_message(Lang):
        await bot.send_message(chat_id=moderation_chat_id, text=Lang.alert.common.error)

    async def _ban(self, message: types.Message, json: dict, Lang):
        await self._group_ban(message=message, Lang=Lang)
        await self._user_ban(message=message, json=json)

    @staticmethod
    async def _group_ban(message: types.Message, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await bot.edit_message_text(chat_id=moderation_chat_id, message_id=message.reply_to_message.message_id,
                                        text=Lang.group.moderation.group.ban)

    @staticmethod
    async def _user_ban(message: types.Message, json: dict):
        users = await pg.select_users(client_id=json.get("client_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormModerationGroup(language=lang_user, url=json.get("url"), name=json.get("name"),
                                                text=message.text)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_ban_platform(),
                                       disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    def register_handlers_ban_platform(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_unban, IsAdmin(), lambda x: x.data.startswith("unbanPlatform"),    state="*")
        dp.register_callback_query_handler(self.menu_ban_cancel, IsAdmin(), lambda x: x.data.startswith("banPlatform"), state="*")
        dp.register_callback_query_handler(self.menu_ban_back, IsAdmin(), text="banBack",                               state="*")

