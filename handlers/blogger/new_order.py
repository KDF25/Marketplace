from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted, \
    MessageToEditNotFound, BotBlocked

from config import bot
from filters.admin import IsAdmin
from filters.form_order import IsPost
from handlers.blogger.all_orders.send_advertiser import SendMessageAdvertiser
from keyboards.inline.blogger.newPost import InlinePostBlogger
from keyboards.inline.common.wallet import InlineWalletUser
from keyboards.inline.group.user import InlineGroupUser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi, pg
from model.all_orders import PostModel
from model.moderation import ModerationModel
from text.blogger.formNewOrder import FormNewOrder
from text.common.formWallet import FormWallet
from text.group.formModeration import FormModerationGroup
from text.language.main import Text_main
from filters.personal_data import IsNumber
from text.fuction.function import TextFunc
from text.group.formWithdraw import FormWithdrawGroup

Txt = Text_main()
func = TextFunc()


class NewPostBlogger(StatesGroup):

    post_level1 = State()
    post_level2 = State()

    # menu project accept
    async def menu_project_accept(self, call: types.CallbackQuery, state: FSMContext):
        print(2, call.data)
        async with state.proxy() as data:
            status, json = await self._post_accept(call, data)
            await self._check_accept(call, data, status, json)

    @staticmethod
    async def _post_accept(call, data):
        blogger_area_id = int(call.data.split("_")[1])
        json = {"blogger_area_id": blogger_area_id}
        status, json = await fastapi.blogger_accept(json=json, token=data.get("token"))

        return status, json

    async def _check_accept(self, call, data, status, json):
        Lang, inline = await self._prepare_blogger(call, data, json)
        if status == 200:
            status, json = await fastapi.project_blogger(blogger_area_id=int(call.data.split("_")[1]), token=data.get("token"))
            await self._accept(call, Lang, inline,  json)
        else:
            await call.answer(text=Lang.alert.common.error, show_alert=True)

    @staticmethod
    async def _prepare_blogger(call, data, json):
        blogger_area_id = int(call.data.split("_")[1])
        Lang = Txt.language[data.get('lang')]
        inline = InlinePostBlogger(language=data.get('lang'),  blogger_area_id=blogger_area_id,
                                   client_id=json.get("advertiser_id"), order_id=json.get("order_id"))
        return Lang, inline

    async def _accept(self, call, Lang, inline, json):
        await self._blogger_accept(call, Lang, inline)
        await self._user_accept(json)

    @staticmethod
    async def _blogger_accept(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.newOrder.blogger.accept,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_accept())

    @staticmethod
    async def _user_accept(json):
        users = await pg.select_users(client_id=json.get("advertiser_id"))

        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormNewOrder(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_accept_advertiser(), disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    # menu project cancel
    async def menu_project_cancel(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            Lang, inline = await self._prepare_cancel(call, data)
            await self._cancel(call, Lang, inline)

    @staticmethod
    async def _prepare_cancel(call, data):
        blogger_area_id = int(call.data.split("_")[1])
        Lang = Txt.language[data.get('lang')]
        inline = InlinePostBlogger(language=data.get('lang'),  blogger_area_id=blogger_area_id)
        return Lang, inline

    @staticmethod
    async def _cancel(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id,  message_id=call.message.message_id,
                                        text=Lang.newOrder.blogger.cancel,  reply_markup=await inline.menu_back())

    # menu project reject
    async def menu_project_reject(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            status, json = await self._post_reject(call, data=data)
            await self._check_reject(call, data, status, json)

    @staticmethod
    async def _post_reject(call, data):
        blogger_area_id = int(call.data.split("_")[1])
        json = {"blogger_area_id": blogger_area_id}
        status, json = await fastapi.blogger_reject(json=json, token=data.get("token"))
        return status, json

    async def _check_reject(self, call, data, status, json):
        Lang, inline = await self._prepare_cancel(call, data)
        if status == 200:
            status, json = await fastapi.project_blogger(blogger_area_id=int(call.data.split("_")[1]), token=data.get("token"))
            await self._reject(call, Lang, json)
        else:
            await call.answer(text=Lang.alert.common.error, show_alert=True)

    async def _reject(self, call, Lang, json):
        await self._blogger_reject(call, Lang)
        await self._user_reject(json)

    @staticmethod
    async def _blogger_reject(call, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.newOrder.blogger.reject,
                                        message_id=call.message.message_id)

    @staticmethod
    async def _user_reject(json):
        users = await pg.select_users(client_id=json.get("advertiser_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormNewOrder(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_reject(), disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    # menu project cancel back
    async def menu_project_cancel_back(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            status, json = await self._project_blogger(call, data)
            form, inline = await self._prepare_back(call, data, json)
            await self._cancel_back(call, form, inline)

    @staticmethod
    async def _project_blogger(call, data):
        blogger_area_id = int(call.data.split("_")[1])
        status, json = await fastapi.project_blogger(blogger_area_id=blogger_area_id, token=data.get("token"))
        return status, json

    @staticmethod
    async def _prepare_back(call, data, json):
        blogger_area_id = int(call.data.split("_")[1])
        form = FormNewOrder(language=data.get('lang'), data=json)
        inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=blogger_area_id,
                                   client_id=json.get("advertiser_id"), order_id=json.get("order_id"))
        return form, inline

    @staticmethod
    async def _cancel_back(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_send_blogger(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_new_post(),
                                        disable_web_page_preview=True)

    # menu post a post
    async def menu_post_post(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['blogger_area_id'] = int(call.data.split("_")[1])
            data["message_id"] = call.message.message_id
            await self._check_date(call, data)

    async def _check_date(self, call, data):
        json = PostModel(blogger_area_id=data.get("blogger_area_id"))
        status, json = await fastapi.send_post(json=json, token=data.get("token"))
        Lang = Txt.language[data.get('lang')]
        if status == 200:
            await self.post_level1.set()
            await self._post_post(call, Lang)
        else:
            await call.answer(show_alert=True, text=Lang.alert.blogger.postDate)

    @staticmethod
    async def _post_post(call, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.newOrder.blogger.postPost,
                                        message_id=call.message.message_id)

    # menu check a post
    async def menu_check_post(self, message: types.Message, state: FSMContext):
        await self.post_level1.set()
        async with state.proxy() as data:
            json = PostModel(blogger_area_id=data.get('blogger_area_id'), post_url= message.text)
            status, json = await fastapi.blogger_check_post(json=json, token=data.get("token"))
            await self._check_check_post(message, data, status, json)
            await state.set_state("MenuBlogger:menuBlogger_level1")

    @staticmethod
    async def _prepare_check_post(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePostBlogger(language=data.get('lang'),  blogger_area_id=data.get('blogger_area_id'))
        return Lang, inline

    async def _check_check_post(self, message, data, status, json):
        Lang, inline = await self._prepare_check_post(data)
        if status == 200:
            status, json = await fastapi.project_blogger(blogger_area_id=data.get('blogger_area_id'), token=data.get("token"))
            await self._check_post(message, data, Lang, json)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.error)

    async def _check_post(self, message, data, Lang, json):
        await self._blogger_check_post(message, data,  Lang)
        await self._user_check_post(json, data)

    @staticmethod
    async def _blogger_check_post(message, data,  Lang):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        await bot.send_message(chat_id=message.from_user.id, text=Lang.newOrder.blogger.checkPost)

    @staticmethod
    async def _user_check_post(json, data):
        users = await pg.select_users(client_id=json.get("advertiser_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormNewOrder(language=lang_user, data=json)
                inline = InlinePostBlogger(language=lang_user, blogger_area_id=data.get('blogger_area_id'),
                                           order_id=json.get("order_id"))
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_check_post(),
                                       reply_markup=await inline.menu_accept_post(), disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    def register_handlers_new_post(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_project_accept, lambda x: x.data.startswith("NewAccept"),          state="*")
        dp.register_callback_query_handler(self.menu_project_cancel, lambda x: x.data.startswith("NewReject"),          state="*")
        dp.register_callback_query_handler(self.menu_project_cancel_back, lambda x: x.data.startswith("RejectBack"),    state="*")
        dp.register_callback_query_handler(self.menu_project_reject, lambda x: x.data.startswith("Reject"),             state="*")

        dp.register_callback_query_handler(self.menu_post_post, lambda x: x.data.startswith("PostPost"),                state="*")
        dp.register_message_handler(self.menu_check_post, IsPost(), content_types=["text"],                                       state=self.post_level1)






