from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, \
    MessageIdentifierNotSpecified, MessageCantBeDeleted, BotBlocked

from config import bot
from handlers.common.new_message import SendMessageAdvertiser
from keyboards.inline.blogger.all_order import InlineAllOrderBlogger
from keyboards.inline.blogger.newPost import InlinePostBlogger
from keyboards.reply.common.user import ReplyUser
from looping import fastapi, pg
from model.all_orders import AllOrder
from model.form_order import OtherModel, ChannelListModel
from model.platform import GetPlatform
from text.blogger.formAllOrder import FormAllOrderBlogger
from text.blogger.formNewOrder import FormNewOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class AllOrderBlogger(StatesGroup):

    all_order_level1 = State()
    platform_level1 = State()

    expects_level1 = State()
    active_level1 = State()
    completed_level1 = State()

    sendAdvertiser_level1 = State()

    # menu all orders
    async def menu_all_orders(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.all_order_level1.set()
        async with state.proxy() as data:
            await self._data_all_orders(data=data)
            await self._get_all_orders(data=data)
            Lang, reply, inline, form = await self._prepare(data=data)
            if isinstance(message, types.Message):
                await self._all_orders(message, form, inline, reply, Lang, data)
            elif isinstance(message, types.CallbackQuery):
                await self._all_orders_back(message, form, inline)

    @staticmethod
    async def _data_all_orders(data):
        data['siteRequest_all'] = OtherModel(offset=0, limit=Txt.limit.blogger.allOrders)

    @staticmethod
    async def _get_all_orders(data):
        params = GetPlatform(offset=data.get('siteRequest_all').get("offset"), limit=data.get('siteRequest_all').get("limit"))
        json = await fastapi.all_orders_blogger(token=data.get("token"), params=params)
        data["allOrder"] = AllOrder(allOrder=json)
        page = data.get('siteRequest_all').get('offset') // data.get('siteRequest_all').get('limit') + 1
        page = page if json['pages'] != 0 else 0
        data["siteRequest_all"].update(ChannelListModel(count=json['count'], pages=json['pages'], page=page))

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        inline = InlineAllOrderBlogger(all_channels=data.get("allOrder").get("allOrder").get("channels", {}),
                                       language=data.get('lang'), siteRequest=data.get('siteRequest_all'))
        form = FormAllOrderBlogger(data=data.get("allOrder").get("allOrder"), language=data.get("lang"))
        return Lang, reply, inline, form

    @staticmethod
    async def _all_orders(message, form, inline, reply, Lang, data):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.activeOrder,
                                          reply_markup=await reply.main_menu())
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_all_orders(),
                                          reply_markup=await inline.menu_all_orders(), disable_web_page_preview=True)
        data['message_id'] = message1.message_id
        data['message_id_None'] = message2.message_id

    @staticmethod
    async def _all_orders_back(message, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                        text=await form.menu_all_orders(), reply_markup=await inline.menu_all_orders())

    # menu all orders turn
    async def menu_all_orders_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_all_orders(call=call, data=data)
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._all_orders_back(call, form, inline)

    async def _callback_all_orders(self, call, data):
        limit = data.get('siteRequest_all').get('limit')
        pages = data.get('siteRequest_all').get('pages')
        page = data.get('siteRequest_all').get('page')
        if call.data == "prev" and page > 1:
            data.get('siteRequest_all')['offset'] -= limit
            data.get('siteRequest_all')['page'] -= 1
            await self._get_all_orders(data=data)
        elif call.data == "next" and page < pages:
            data.get('siteRequest_all')['offset'] += limit
            data.get('siteRequest_all')['page'] += 1
            await self._get_all_orders(data=data)

    # menu platform
    async def menu_platform(self, call: types.CallbackQuery, state: FSMContext):
        await self.platform_level1.set()
        async with state.proxy() as data:
            if call.data != "back":
                data.get("allOrder")["current_platform"] = {}
                data.get("allOrder")["current_platform"]["id"] = int(call.data.split("_")[1])
            await self._get_platform(data=data)
            inline, form = await self._prepare_platform(data)
            await self._platform(call, form, inline)

    @staticmethod
    async def _get_platform(data):
        for channel in data.get("allOrder").get("allOrder").get("channels"):
            if channel.get("area_id") == data.get("allOrder").get("current_platform").get("id"):
                data.get("allOrder")["current_platform"] = channel
                return channel

    @staticmethod
    async def _prepare_platform(data):
        inline = InlineAllOrderBlogger(channel=data.get("allOrder").get("current_platform"), language=data.get('lang'))
        form = FormAllOrderBlogger(data=data.get("allOrder").get("current_platform"), language=data.get("lang"))
        return inline, form

    @staticmethod
    async def _platform(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_platform(), reply_markup=await inline.menu_platform(),
                                        disable_web_page_preview=True)

    # menu active orders
    async def menu_active_orders(self, call: types.CallbackQuery, state: FSMContext):
        await self.active_level1.set()
        async with state.proxy() as data:
            await self._data_orders(data=data)
            await self._get_active_orders(data)
            inline, form = await self._prepare_orders(data=data)
            await self._active_orders(call, form, inline)

    @staticmethod
    async def _data_orders(data):
        data['siteRequest'] = OtherModel(offset=0, limit=Txt.limit.blogger.orders)

    @staticmethod
    async def _site_request(data, json):
        data.get("allOrder").update(AllOrder(orders=json['channels']))
        page = data.get('siteRequest').get('offset') // data.get('siteRequest').get('limit') + 1
        page = page if json['pages'] != 0 else 0
        data["siteRequest"].update(ChannelListModel(count=json['count'], pages=json['pages'], page=page))

    async def _get_active_orders(self, data):
        params = GetPlatform(area_id=data.get("allOrder").get("current_platform").get('area_id'),
                             offset=data.get('siteRequest').get("offset"),
                             limit=data.get('siteRequest').get("limit"))
        json = await fastapi.all_active_blogger(token=data.get("token"), params=params)
        await self._site_request(data, json)

    @staticmethod
    async def _prepare_orders(data):
        inline = InlineAllOrderBlogger(orders=data.get("allOrder").get("orders"), language=data.get('lang'),
                                       current_id=data.get("allOrder").get("current_platform").get('area_id'),
                                       siteRequest=data.get('siteRequest'))
        form = FormAllOrderBlogger(data=data.get("allOrder").get("current_platform"), language=data.get("lang"))
        return inline, form

    @staticmethod
    async def _active_orders(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_active(), reply_markup=await inline.menu_orders(),
                                        disable_web_page_preview=True)

    # menu active orders turn
    async def menu_active_orders_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_orders(call=call, data=data)
            await self._get_active_orders(data=data)
            inline, form = await self._prepare_orders(data=data)
            await self._active_orders(call, form, inline)

    @staticmethod
    async def _callback_orders(call, data):
        limit = data.get('siteRequest').get('limit')
        pages = data.get('siteRequest').get('pages')
        page = data.get('siteRequest').get('page')
        if call.data == "prev" and page > 1:
            data.get('siteRequest')['offset'] -= limit
            data.get('siteRequest')['page'] -= 1
        elif call.data == "next" and page < pages:
            data.get('siteRequest')['offset'] += limit
            data.get('siteRequest')['page'] += 1

    # menu active project
    async def menu_active_project(self, call: types.CallbackQuery, state: FSMContext):
        await self.active_level1.set()
        async with state.proxy() as data:
            status, json = await self._project_blogger(call, data)
            form, inline = await self._prepare_active_project(call, data, json)
            if call.data.split("_")[0] == "order":
                if json.get('post_url') is None:
                    await self._active_project(call, form, inline)
                else:
                    await self._check_post(call, form, inline)
            else:
                await self._active_project_back(call, form, inline)

    @staticmethod
    async def _prepare_active_project(call, data, json):
        blogger_area_id = int(call.data.split("_")[1])
        data["blogger_area_id"] = blogger_area_id
        form = FormNewOrder(language=data.get('lang'), data=json)
        inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=blogger_area_id,
                                   order_id=json.get("order_id"), client_id=json.get("advertiser_id"))
        return form, inline

    @staticmethod
    async def _check_post(call, form, inline):
        await call.answer()
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_review_post(),
                               reply_markup=await inline.menu_check_post2(), disable_web_page_preview=True)

    @staticmethod
    async def _active_project(call, form, inline):
        await call.answer()
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_accept(),
                               reply_markup=await inline.menu_accept(), disable_web_page_preview=True)

    @staticmethod
    async def _active_project_back(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_accept(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_accept(),
                                        disable_web_page_preview=True)

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
                                        text=Lang.newOrder.blogger.cancel,  reply_markup=await inline.menu_back2())

    # menu expects orders
    async def menu_expects_orders(self, call: types.CallbackQuery, state: FSMContext):
        await self.expects_level1.set()
        async with state.proxy() as data:
            await self._data_orders(data=data)
            await self._get_expects_orders(data)
            inline, form = await self._prepare_orders(data=data)
            await self._expects_orders(call, form, inline)

    async def _get_expects_orders(self, data):
        params = GetPlatform(area_id=data.get("allOrder").get("current_platform").get('area_id'),
                             offset=data.get('siteRequest').get("offset"),
                             limit=data.get('siteRequest').get("limit"))
        json = await fastapi.all_wait_blogger(token=data.get("token"), params=params)
        await self._site_request(data,json)

    @staticmethod
    async def _expects_orders(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_expects(), reply_markup=await inline.menu_orders(),
                                        disable_web_page_preview=True)

    # menu expects orders turn
    async def menu_expects_orders_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_orders(call=call, data=data)
            await self._get_expects_orders(data=data)
            inline, form = await self._prepare_orders(data=data)
            await self._expects_orders(call, form, inline)

    # menu new project
    async def menu_new_project(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            status, json = await self._project_blogger(call, data)
            form, inline = await self._prepare_new_project(call, data, json)
            await self._new_project(call, form, inline)

    @staticmethod
    async def _project_blogger(call, data):
        blogger_area_id = int(call.data.split("_")[1])
        status, json = await fastapi.project_blogger(blogger_area_id=blogger_area_id, token=data.get("token"))
        return status, json

    @staticmethod
    async def _prepare_new_project(call, data, json):
        blogger_area_id = int(call.data.split("_")[1])
        form = FormNewOrder(language=data.get('lang'), data=json)
        inline = InlinePostBlogger(language=data.get('lang'), order_id=json.get("order_id"), blogger_area_id=blogger_area_id)
        return form, inline

    @staticmethod
    async def _new_project(call, form, inline):
        await call.answer()
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_send_blogger(),
                               reply_markup=await inline.menu_new_post(), disable_web_page_preview=True)

    # menu send advertiser
    async def menu_send_advertiser(self, call: types.CallbackQuery, state: FSMContext):
        await self.sendAdvertiser_level1.set()
        async with state.proxy() as data:
            if call.data.split("_")[0] == "SendAdvertiser":
                data["blogger_area_id"] = int(call.data.split("_")[1])
                data["message_id"] = call.message.message_id
            Lang, inline = await self._prepare_send_advertiser(data)
            await self._send_advertiser(call, Lang, inline)

    @staticmethod
    async def _prepare_send_advertiser(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data.get("blogger_area_id"))
        return Lang, inline

    @staticmethod
    async def _send_advertiser(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.newOrder.blogger.sendMessage, reply_markup=await inline.menu_back3())

    # menu send message
    async def menu_end(self, message: types.Message, state: FSMContext):
        await self.active_level1.set()
        async with state.proxy() as data:
            status, json = await self._project(data)
            send = SendMessageAdvertiser(data=json, text=message.html_text, blogger_area_id=data.get("blogger_area_id"))
            await send.answer()
            Lang = Txt.language[data.get('lang')]
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.newOrder.blogger.end)

    @staticmethod
    async def _project(data):
        status, json = await fastapi.project_blogger(blogger_area_id=int(data.get("blogger_area_id")), token=data.get("token"))
        return status, json

    # menu completed orders
    async def menu_completed_orders(self, call: types.CallbackQuery, state: FSMContext):
        await self.completed_level1.set()
        async with state.proxy() as data:
            await self._data_orders(data=data)
            await self._get_completed_orders(data)
            inline, form = await self._prepare_orders(data=data)
            await self._completed_orders(call, form, inline)

    async def _get_completed_orders(self, data):
        params = GetPlatform(area_id=data.get("allOrder").get("current_platform").get('area_id'),
                             offset=data.get('siteRequest').get("offset"),
                             limit=data.get('siteRequest').get("limit"))
        json = await fastapi.all_completed_blogger(token=data.get("token"), params=params)
        await self._site_request(data, json)

    @staticmethod
    async def _completed_orders(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_completed(), reply_markup=await inline.menu_orders(),
                                        disable_web_page_preview=True)

    # menu completed orders turn
    async def menu_completed_orders_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_orders(call=call, data=data)
            await self._get_completed_orders(data=data)
            inline, form = await self._prepare_orders(data=data)
            await self._completed_orders(call, form, inline)

    # menu completed project
    async def menu_completed_project(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            status, json = await self._project_blogger(call, data)
            form, inline = await self._prepare_new_project(call, data, json)
            await self._completed_project(call, form)

    @staticmethod
    async def _completed_project(call, form):
        await call.answer()
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_completed(),
                               disable_web_page_preview=True)

    @staticmethod
    async def menu_zero_count(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            await call.answer(show_alert=True, text=Lang.alert.common.zeroCount)

    def register_handlers_all_orders_blogger(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_all_orders, text=Txt.menu.activeOrder,                                    state="MenuBlogger:menuBlogger_level1")
        dp.register_callback_query_handler(self.menu_all_orders_turn, text=["prev", "next"],                            state=self.all_order_level1)
        dp.register_callback_query_handler(self.menu_all_orders, text="back",                                           state=self.platform_level1)

        dp.register_callback_query_handler(self.menu_platform, lambda x: x.data.startswith("platform"),                 state=self.all_order_level1)
        dp.register_callback_query_handler(self.menu_platform, text="back",                                             state=[self.active_level1, self.expects_level1, self.completed_level1])

        dp.register_callback_query_handler(self.menu_active_orders, text="active",                                      state=self.platform_level1)
        dp.register_callback_query_handler(self.menu_active_orders_turn, text=["prev", "next"],                         state=self.active_level1)

        dp.register_callback_query_handler(self.menu_expects_orders, text="expects",                                    state=self.platform_level1)
        dp.register_callback_query_handler(self.menu_expects_orders_turn, text=["prev", "next"],                        state=self.expects_level1)

        dp.register_callback_query_handler(self.menu_completed_orders, text="completed",                                state=self.platform_level1)
        dp.register_callback_query_handler(self.menu_completed_orders_turn, text=["prev", "next"],                      state=self.completed_level1)

        dp.register_callback_query_handler(self.menu_zero_count, text="zeroCount",                                      state=self.platform_level1)

        dp.register_callback_query_handler(self.menu_active_project, lambda x: x.data.startswith("order"),              state=self.active_level1)
        dp.register_callback_query_handler(self.menu_active_project, lambda x: x.data.startswith("PostBack"),           state=[self.sendAdvertiser_level1, "*"])
        dp.register_callback_query_handler(self.menu_project_cancel, lambda x: x.data.startswith("PostCancel"),         state="*")

        dp.register_callback_query_handler(self.menu_new_project, lambda x: x.data.startswith("order"),                 state=self.expects_level1)
        dp.register_callback_query_handler(self.menu_completed_project, lambda x: x.data.startswith("order"),           state=self.completed_level1)

        dp.register_callback_query_handler(self.menu_send_advertiser, lambda x: x.data.startswith("SendAdvertiser"),    state=self.active_level1)
        dp.register_message_handler(self.menu_end, content_types=["text"],                                              state=self.sendAdvertiser_level1)


