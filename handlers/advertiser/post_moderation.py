from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, BotBlocked

from config import bot, moderation_chat_id
from keyboards.inline.blogger.newPost import InlinePostBlogger
from looping import fastapi, pg
from model.all_orders import PostModel
from text.advertiser.formPostModeration import FormPostModeration
from text.blogger.formNewOrder import FormNewOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class PostModerationAdvertiser(StatesGroup):

    # menu accept
    async def menu_accept(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["blogger_area_id"] = int(call.data.split("_")[1])
            json = PostModel(blogger_area_id=data.get("blogger_area_id"))
            status, json = await fastapi.advertiser_accept(json=json, token=data.get("token"))
            data["area_id"] = json.get("area_id")
            await self._check_accept(call, data, status)

    async def _check_accept(self, call, data, status):
        Lang, inline = await self._prepare_accept(data)
        if status == 200:
            status, json = await fastapi.project_blogger(blogger_area_id=data.get('blogger_area_id'), token=data.get("token"))
            await self._accept(call, Lang, inline, json)
        else:
            await bot.send_message(chat_id=call.from_user.id, text=Lang.alert.common.error)

    async def _accept(self, call, Lang, inline, json):
        await self._advertiser_accept(call, Lang, inline)
        await self._user_accept(json)

    @staticmethod
    async def _advertiser_accept(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id,  text=Lang.newOrder.advertiser.postAccept,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_rate_post())

    @staticmethod
    async def _prepare_accept(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePostBlogger(language=data.get("lang"), area_id=data.get("area_id"))
        return Lang, inline

    @staticmethod
    async def _user_accept(json):
        users = await pg.select_users(client_id=json.get("blogger_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form = FormPostModeration(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form.menu_accept(), disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    # menu rate post
    async def menu_rate_post(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["area_id"] = int(call.data.split("_")[1])
            Lang, inline = await self._prepare_accept(data)
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.newOrder.advertiser.rate,
                                            message_id=call.message.message_id,  reply_markup=await inline.menu_rate())

    # menu rate
    async def menu_rate(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["area_id"] = int(call.data.split("_")[2])
            data["rate"] = int(call.data.split("_")[1])
            Lang, inline = await self._prepare_accept(data)
            json = PostModel(area_id=data.get("area_id"), rate=data.get("rate"))
            await fastapi.rate_post(json=json, token=data.get("token"))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.newOrder.advertiser.thanks,
                                            message_id=call.message.message_id)

    # menu cancel
    @staticmethod
    async def menu_cancel(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang = Txt.language[data.get('lang')]
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"])
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=Lang.newOrder.advertiser.postCancel, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_back_accept_post())

    # menu cancel back
    @staticmethod
    async def menu_cancel_back(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["blogger_area_id"] = int(call.data.split("_")[1])
            status, json = await fastapi.project_blogger(blogger_area_id=data.get('blogger_area_id'), token=data.get("token"))
            form_user = FormNewOrder(language=data.get('lang'), data=json)
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data.get('blogger_area_id'),
                                       order_id=json.get("order_id"))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form_user.menu_check_post(), disable_web_page_preview=True,
                                            reply_markup=await inline. menu_accept_post())

    # menu reject
    async def menu_reject(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["blogger_area_id"] = int(call.data.split("_")[1])
            json = PostModel(blogger_area_id=data.get("blogger_area_id"))
            status, json = await fastapi.advertiser_reject(json=json, token=data.get("token"))
            await self._check_reject(call, data, status)

    async def _check_reject(self, call, data, status):
        Lang = Txt.language[data.get('lang')]
        if status == 200:
            status, json = await fastapi.project_blogger(blogger_area_id=int(call.data.split("_")[1]), token=data.get("token"))
            await self._reject(data, call, Lang, json)
        else:
            await call.answer(text=Lang.alert.common.error, show_alert=True)

    async def _reject(self, data, call, Lang, json):
        await self._advertiser_reject(call, Lang)
        await self._user_reject(json)
        await self._group(data, json)

    @staticmethod
    async def _advertiser_reject(call, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.newOrder.advertiser.postReject)

    @staticmethod
    async def _user_reject(json):
        users = await pg.select_users(client_id=json.get("blogger_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form = FormPostModeration(language=lang_user, data=json)
                inline = InlinePostBlogger(language=lang_user, order_id=json.get("order_id"))
                await bot.send_message(chat_id=user_id[0], text=await form.menu_reject(), disable_web_page_preview=True,
                                       reply_markup=await inline.menu_check_post())
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    @staticmethod
    async def _group(data, json):
        lang_user = 'rus'
        form = FormPostModeration(language=lang_user, data=json)
        inline = InlinePostBlogger(language=lang_user, order_id=json.get("order_id"), blogger_area_id=data.get("blogger_area_id"))
        await bot.send_message(chat_id=moderation_chat_id, text=await form.menu_moderation(),
                               disable_web_page_preview=True, reply_markup=await inline.menu_moderation_post())

    @staticmethod
    async def _project_blogger(blogger_area_id, data):
        status, json = await fastapi.project_blogger(blogger_area_id=blogger_area_id, token=data.get("token"))
        return status, json


    async def default(self, call: types.CallbackQuery, state: FSMContext):
        print(call.data, await state.get_state())

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_accept, lambda x: x.data.startswith("PostAdvertiserAccept"),       state="*")
        dp.register_callback_query_handler(self.menu_rate_post, lambda x: x.data.startswith("RatePost"),                state="*")
        dp.register_callback_query_handler(self.menu_rate, lambda x: x.data.startswith("RatePoint"),                    state="*")

        dp.register_callback_query_handler(self.menu_cancel, lambda x: x.data.startswith("PostAdvertiserReject"),       state="*")
        dp.register_callback_query_handler(self.menu_cancel_back, lambda x: x.data.startswith("BackPostAdvertiser"),    state="*")
        dp.register_callback_query_handler(self.menu_reject, lambda x: x.data.startswith("ModerationPostAdvertiser"),   state="*")
        # dp.register_callback_query_handler(self.default, lambda x: x.data.startswith('') , state='*')
