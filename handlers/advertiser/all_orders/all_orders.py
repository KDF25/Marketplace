from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageIdentifierNotSpecified, \
    MessageToDeleteNotFound, MessageCantBeDeleted

from config import bot
from handlers.advertiser.all_orders.send_blogger import SendMessageBlogger
from keyboards.inline.advertiser.all_order import InlineAllOrderAdvertiser
from keyboards.inline.advertiser.form_order import InlineFormOrderAdvertiser
from keyboards.reply.advertiser.advertiser import ReplyAdvertiser
from looping import fastapi
from model.all_orders import AllOrder
from model.basket import Basket
from model.form_order import OtherModel, ChannelListModel
from model.platform import GetPlatform
from text.advertiser.formAllOrder import FormAllOrderAdvertiser
from text.advertiser.formOrder import FormOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class AllOrderAdvertiser(StatesGroup):

    all_order_level1 = State()
    platform_level1 = State()

    active_level1 = State()
    active_level2 = State()

    completed_level1 = State()
    completed_level2 = State()

    sendBlogger_level1 = State()
    sendBlogger_level2 = State()
    sendBlogger_level3 = State()

    # menu all orders
    async def menu_all_orders(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.all_order_level1.set()
        async with state.proxy() as data:
            await self._get_all_orders(data)
            Lang, reply, inline, form = await self._prepare(data)
            if isinstance(message, types.Message):
                await self._all_orders(message, data, Lang, form, reply, inline)
            elif isinstance(message, types.CallbackQuery):
                await self._all_orders_back(message, form, inline)

    @staticmethod
    async def _get_all_orders(data):
        json = await fastapi.all_orders_advertiser(token=data.get("token"))
        data["allOrder"] = AllOrder(allOrder=json)

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyAdvertiser(language=data.get('lang'))
        inline = InlineAllOrderAdvertiser(all_orders=data.get("allOrder").get("allOrder"), language=data.get('lang'))
        form = FormAllOrderAdvertiser(data=data.get("allOrder").get("allOrder"), language=data.get("lang"))
        return Lang, reply, inline, form

    @staticmethod
    async def _all_orders(message, data, Lang, form, reply, inline):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.activeOrder,
                                          reply_markup=await reply.main_menu())
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_all_orders(),
                                          reply_markup=await inline.menu_all_orders())
        data['message_id'] = message1.message_id
        data['message_id_None'] = message2.message_id

    @staticmethod
    async def _all_orders_back(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_all_orders(), reply_markup=await inline.menu_all_orders())

    # menu active orders
    async def menu_active_orders(self, call: types.CallbackQuery, state: FSMContext):
        await self.active_level1.set()
        async with state.proxy() as data:
            await self._data_orders(data=data)
            await self._get_active_orders(data)
            Lang, inline = await self._prepare_orders(data)
            await self._active_orders(call, Lang, inline)

    @staticmethod
    async def _data_orders(data):
        data['siteRequest'] = OtherModel(offset=0, limit=Txt.limit.advertiser.orders)

    async def _get_active_orders(self, data):
        params = GetPlatform(offset=data.get('siteRequest').get("offset"), limit=data.get('siteRequest').get("limit"))
        json = await fastapi.all_active_advertiser(token=data.get("token"), params=params)
        await self._site_request(data=data, json=json)

    @staticmethod
    async def _site_request(data, json):
        data.get("allOrder").update(AllOrder(orders=json['orders']))
        page = data.get('siteRequest').get('offset') // data.get('siteRequest').get('limit') + 1
        page = page if json['pages'] != 0 else 0
        data["siteRequest"].update(ChannelListModel(count=json['count'], pages=json['pages'], page=page))

    @staticmethod
    async def _prepare_orders(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlineAllOrderAdvertiser(orders=data.get("allOrder").get("orders"), language=data.get('lang'),
                                          siteRequest=data.get('siteRequest'))
        return Lang, inline

    @staticmethod
    async def _active_orders(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.allOrder.active + "👇", reply_markup=await inline.menu_orders())

    # menu active orders turn
    async def menu_active_orders_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_orders(call=call, data=data)
            await self._get_active_orders(data=data)
            Lang, inline = await self._prepare_orders(data)
            await self._active_orders(call, Lang, inline)

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

    # menu active orders
    async def menu_active_project(self, call: types.CallbackQuery, state: FSMContext):
        await self.active_level2.set()
        async with state.proxy() as data:
            await self._get_campaign(call, data)
            form, inline = await self._prepare_project(call, data)
            await self._active_project(call, form, inline)

    @staticmethod
    async def _get_campaign(call, data):
        if call.data != "back":
            json = Basket(order_id=int(call.data.split("_")[1]), language=data.get("lang"))
            json = await fastapi.get_basket(json=json, token=data.get("token"))
            data.get("allOrder").update(AllOrder(orders=json))

    @staticmethod
    async def _prepare_project(call, data):
        if call.data != "back":
            order_id = int(call.data.split("_")[1])
            data.get("allOrder").update(AllOrder(current_channel=order_id))
        form = FormAllOrderAdvertiser(language=data.get("lang"), data=data.get("allOrder").get("orders"))
        inline = InlineAllOrderAdvertiser(orders=data.get("allOrder").get("orders"), language=data.get('lang'),
                                          order_id=data.get("allOrder").get("current_channel"))
        return form, inline

    @staticmethod
    async def _active_project(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_active_project(), reply_markup=await inline.menu_active_project(),
                                        disable_web_page_preview=True)

    # menu completed orders
    async def menu_completed_orders(self, call: types.CallbackQuery, state: FSMContext):
        await self.completed_level1.set()
        async with state.proxy() as data:
            await self._get_completed_orders(data)
            Lang, inline = await self._prepare_orders(data)
            await self._completed_orders(call, Lang, inline)

    async def _get_completed_orders(self, data):
        params = GetPlatform(offset=data.get('siteRequest').get("offset"), limit=data.get('siteRequest').get("limit"))
        json = await fastapi.all_completed_advertiser(token=data.get("token"), params=params)
        await self._site_request(data, json)

    @staticmethod
    async def _completed_orders(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.allOrder.completed + "👇", reply_markup=await inline.menu_orders())

    # menu active orders turn
    async def menu_completed_orders_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_orders(call=call, data=data)
            await self._get_completed_orders(data=data)
            Lang, inline = await self._prepare_orders(data)
            await self._completed_orders(call, Lang, inline)

    # menu active orders
    async def menu_completed_project(self, call: types.CallbackQuery, state: FSMContext):
        await self.completed_level2.set()
        async with state.proxy() as data:
            await self._get_campaign(call, data)
            form, inline = await self._prepare_project(call, data)
            await self._completed_project(call, form, inline)

    @staticmethod
    async def _completed_project(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_active_project(), reply_markup=await inline.menu_completed_project(),
                                        disable_web_page_preview=True)

    # menu zero count
    @staticmethod
    async def menu_zero_count(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            await call.answer(show_alert=True, text=Lang.alert.common.zeroCount)

    # menu send blogger
    async def menu_send_blogger(self, call: types.CallbackQuery, state: FSMContext):
        await self.sendBlogger_level1.set()
        async with state.proxy() as data:
            await self._channel_list(data)
            Lang, inline = await self._prepare_send_blogger(data)
            await self._send_blogger(call, Lang, inline)

    @staticmethod
    async def _channel_list(data):
        if data.get("allOrder").get("channels") is None:
            data.get("allOrder").update(AllOrder(channels=[]))

    @staticmethod
    async def _prepare_send_blogger(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlineAllOrderAdvertiser(orders=data.get("allOrder").get("orders"), language=data.get('lang'),
                                          channels=data.get("allOrder").get("channels"))
        return Lang, inline

    @staticmethod
    async def _send_blogger(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.newOrder.advertiser.sendBlogger,
                                        reply_markup=await inline.menu_send_blogger())

    # menu send blogger change
    async def menu_send_blogger_change(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_channel(call, data)
            Lang, inline = await self._prepare_send_blogger(data)
            await self._send_blogger(call, Lang, inline)

    @staticmethod
    async def _change_channel(call, data):
        area_id = int(call.data.split("_")[1])
        if area_id in data.get("allOrder").get("channels"):
            data.get("allOrder")["channels"].remove(area_id)
        elif area_id not in data.get("allOrder").get("channels"):
            data.get("allOrder").get("channels").append(area_id)

    # menu send message
    async def menu_send_message(self, call: types.CallbackQuery, state: FSMContext):
        print(2)
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            await self._check_channel_list(call, data)

    async def _check_channel_list(self, call, data):
        Lang, inline = await self._prepare_send_message(data)
        if len(data.get("allOrder").get("channels")) == 0:
            await call.answer(show_alert=True, text=Lang.alert.common.zeroCount)
        else:
            await self.sendBlogger_level2.set()
            await self._send_message(call, Lang, inline)

    @staticmethod
    async def _prepare_send_message(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlineAllOrderAdvertiser(orders=data.get("allOrder").get("orders"), language=data.get('lang'),
                                          channels=data.get("allOrder").get("channels"))
        return Lang, inline

    @staticmethod
    async def _send_message(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.newOrder.advertiser.sendMessage,
                                        reply_markup=await inline.menu_back())

    # menu send message
    async def menu_end(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            json = await self._get_list_client_id(data)
            send = SendMessageBlogger(data=json, text=message.html_text, token=data.get("token"))
            await send.send_blogger()
            Lang = Txt.language[data.get('lang')]
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.newOrder.advertiser.end)

    @staticmethod
    async def _get_list_client_id(data):
        json = AllOrder(order_id=data.get("allOrder").get("current_channel"), channels=data.get("allOrder").get("channels"))
        json = await fastapi.get_list_client_id(json=json, token=data.get("token"))
        return json

    def register_handlers_all_orders_advertiser(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_all_orders, text=Txt.menu.activeOrder,                                    state="MenuAdvertiser:menuAdvertiser_level1")
        dp.register_callback_query_handler(self.menu_all_orders, text="back",                                           state=[self.active_level1, self.completed_level1])

        dp.register_callback_query_handler(self.menu_active_orders, text="active",                                      state=self.all_order_level1)
        dp.register_callback_query_handler(self.menu_active_orders_turn, text=["prev", "next"],                         state=self.active_level1)
        dp.register_callback_query_handler(self.menu_active_orders, text="back",                                        state=self.active_level2)

        dp.register_callback_query_handler(self.menu_completed_orders, text="completed",                                state=self.all_order_level1)
        dp.register_callback_query_handler(self.menu_completed_orders_turn, text=["prev", "next"],                      state=self.completed_level1)
        dp.register_callback_query_handler(self.menu_completed_orders, text="back",                                     state=self.completed_level2)

        dp.register_callback_query_handler(self.menu_zero_count, text="zeroCount",                                      state=self.all_order_level1)

        dp.register_callback_query_handler(self.menu_active_project, lambda x: x.data.startswith("order"),              state=self.active_level1)
        dp.register_callback_query_handler(self.menu_active_project, text="back",                                       state=self.sendBlogger_level1)
        dp.register_callback_query_handler(self.menu_completed_project, lambda x: x.data.startswith("order"),           state=self.completed_level1)

        dp.register_callback_query_handler(self.menu_send_blogger, text="SendBlogger",                                  state=self.active_level2)
        dp.register_callback_query_handler(self.menu_send_blogger, text="back",                                         state=self.sendBlogger_level2)
        dp.register_callback_query_handler(self.menu_send_blogger_change, lambda x: x.data.startswith("channel"),       state=self.sendBlogger_level1)

        dp.register_callback_query_handler(self.menu_send_message, text="SendBloggerAccept",                            state=self.sendBlogger_level1)
        dp.register_message_handler(self.menu_end, IsReplyFilter(is_reply=True), content_types=["text"],                state=self.sendBlogger_level2)




