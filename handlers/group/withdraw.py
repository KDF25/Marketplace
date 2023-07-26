from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import *

from config import bot, moderation_chat_id
from filters.admin import IsAdmin
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi, pg
from model.wallet import WalletModel
from text.fuction.function import TextFunc
from text.group.formWithdraw import FormWithdrawGroup
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class WithdrawGroup(StatesGroup):

    # menu withdraw accept
    async def menu_withdraw_accept(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuGroup:start")
        print(await state.get_state())
        status, json = await self._withdraw_accept(call=call)
        await self._check_accept(call=call, status=status, json=json)

    @staticmethod
    async def _withdraw_accept(call: types.CallbackQuery):
        json = WalletModel(journal_id=int(call.data.split("_")[1]))
        status, json = await fastapi.withdraw_accept(json=json)
        return status, json

    @staticmethod
    async def _prepare_group():
        lang = "rus"
        Lang: Model = Txt.language[lang]
        inline = InlineGroupUser(language=lang)
        return Lang, inline

    async def _check_accept(self, call: types.CallbackQuery, status: int, json: dict):
        Lang, inline = await self._prepare_group()
        if status == 200:
            await self._accept(call=call, Lang=Lang, json=json)
        else:
            await self._error(call=call, Lang=Lang)

    async def _accept(self, call: types.CallbackQuery, json: dict , Lang):
        await self._group_accept(call=call, Lang=Lang)
        await self._user_accept(json=json)

    @staticmethod
    async def _error(call: types.CallbackQuery, Lang):
        await call.answer(text=Lang.alert.common.error, show_alert=True)

    @staticmethod
    async def _group_accept(call: types.CallbackQuery, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=moderation_chat_id, text=Lang.group.withdraw.group.accept,
                                        message_id=call.message.message_id, disable_web_page_preview=True)

    @staticmethod
    async def _user_accept(json: dict):
        users = await pg.select_users(client_id=json.get("client_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormWithdrawGroup(language=lang_user, amount=json.get("amount"))
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_accept_user())
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)
            except ChatNotFound:
                pass

    # menu withdraw cancel
    async def menu_withdraw_cancel(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuGroup:start")
        Lang, inline = await self._prepare_group()
        await self._cancel(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _cancel( call: types.CallbackQuery, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            text = f"{call.message.text}\n\n{Lang.group.withdraw.group.reason}\n\n#journalId_{call.data.split('_')[1]}"
            await bot.edit_message_text(chat_id=moderation_chat_id, text=text, entities=call.message.entities,
                                        reply_markup=await inline.menu_withdraw_back(),
                                        message_id=call.message.message_id)

    # menu withdraw cancel back
    async def menu_withdraw_cancel_back(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuGroup:start")
        journal_id = await self._unpack_call(call=call)
        Lang, inline = await self._prepare_cancel_back(journal_id=journal_id)
        await self._cancel_back(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _unpack_call(call: types.CallbackQuery):
        entities = call.message.entities
        journal_id = int(entities[-1].get_text(call.message.text).split('_')[1])
        return journal_id

    @staticmethod
    async def _prepare_cancel_back(journal_id: int):
        lang = "rus"
        Lang: Model = Txt.language[lang]
        inline = InlineGroupUser(language=lang, enter_id=journal_id)
        return Lang, inline

    @staticmethod
    async def _cancel_back(call: types.CallbackQuery, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            text = call.message.text.split(Lang.group.withdraw.group.reason)[0]
            await bot.edit_message_text(chat_id=moderation_chat_id, text=text, entities=call.message.entities,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_withdraw())

    # menu withdraw reject
    async def menu_withdraw_reject(self, message: types.Message):
        await self._answer(message=message)

    async def _answer(self, message: types.Message):
        try:
            journal_id = await self._unpack_message(message=message)
            status, json = await self._post_reject(journal_id=journal_id, message=message)
            await self._check_reject(message=message, status=status, json=json)
        except BaseException:
            Lang, inline = await self._prepare_group()
            await self._error_message(Lang=Lang)

    @staticmethod
    async def _unpack_message(message: types.Message):
        entities = message.reply_to_message.entities
        journal_id = int(entities[-1].get_text(message.reply_to_message.text).split('_')[1])
        return journal_id

    @staticmethod
    async def _post_reject(journal_id: int, message: types.Message):
        json = WalletModel(journal_id=journal_id, reason=message.text)
        status, json = await fastapi.withdraw_reject(json=json)
        return status, json

    async def _check_reject(self, message: types.Message, status: int, json: dict):
        Lang, inline = await self._prepare_group()
        if status == 200:
            await self._reject(message=message, json=json, Lang=Lang)
        else:
            await self._error_message(Lang=Lang)

    @staticmethod
    async def _error_message(Lang):
        await bot.send_message(chat_id=moderation_chat_id, text=Lang.alert.common.error)

    async def _reject(self, message: types.Message, json: dict, Lang):
        await self._group_reject(message=message, Lang=Lang)
        await self._user_reject(message=message, json=json)

    @staticmethod
    async def _group_reject(message: types.Message, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await bot.edit_message_text(chat_id=moderation_chat_id, message_id=message.reply_to_message.message_id,
                                        text=Lang.group.withdraw.group.reject)

    @staticmethod
    async def _user_reject( message: types.Message, json: dict):
        users = await pg.select_users(client_id=json.get("client_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormWithdrawGroup(language=lang_user, text=message.text)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_reject_user())
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    def register_handlers_withdraw(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_withdraw_accept, IsAdmin(),
                                           lambda x: x.data.startswith("withdrawAccept"),                               state="*")

        dp.register_callback_query_handler(self.menu_withdraw_cancel, IsAdmin(),
                                           lambda x: x.data.startswith("withdrawReject"),                               state="*")
        dp.register_callback_query_handler(self.menu_withdraw_cancel_back, IsAdmin(), text="withdrawBack",              state="*")

