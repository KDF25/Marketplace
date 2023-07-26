from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import *

from config import bot
from keyboards.inline.blogger.newPost import InlinePostBlogger
from looping import fastapi, pg
from text.blogger.formNewOrder import FormNewOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class SendMessageAdvertiser:

    def __init__(self, text, blogger_area_id: int, data: dict):
        self.__user_id = None
        self.__text = text
        self.__blogger_area_id = blogger_area_id
        self.__data = data

    async def answer(self):
        users = await pg.select_users(client_id=self.__data.get("advertiser_id"))
        for user_id in users:
            self.__user_id = user_id[0]
            await self._post()

    async def _post(self):
        try:
            await self._prepare_post()
            await self._send_post()
        except BotBlocked:
            await pg.block_status(user_id=self.__user_id, status=False)

    async def _prepare_post(self):
        lang = await pg.select_language(user_id=self.__user_id)
        self.__form = FormNewOrder(data=self.__data, language=lang)
        self.__inline = InlinePostBlogger(language=lang, order_id=self.__data.get("order_id"),
                                          blogger_area_id=self.__blogger_area_id)

    async def _send_post(self):
        text = await self.__form.menu_send_advertiser(message_text=self.__text)
        await bot.send_message(chat_id=self.__user_id, text=text,  reply_markup=await self.__inline.menu_send_advertiser(),
                               disable_web_page_preview=True)


class SendMessageBlogger:

    def __init__(self, text, blogger_area_id: int, data: dict):
        self.__user_id = None
        self.__text = text
        self.__blogger_area_id = blogger_area_id
        self.__data = data

    async def answer(self):
        users = await pg.select_users(client_id=self.__data.get("blogger_id"))
        for user_id in users:
            self.__user_id = user_id[0]
            await self._post()

    async def _post(self):
        try:
            await self._prepare_post()
            await self._send_post()
        except BotBlocked:
            await pg.block_status(user_id=self.__user_id, status=False)

    async def _prepare_post(self):
        lang = await pg.select_language(user_id=self.__user_id)
        self.__form = FormNewOrder(data=self.__data, language=lang)
        self.__inline = InlinePostBlogger(language=lang, order_id=self.__data.get("order_id"),
                                          blogger_area_id=self.__blogger_area_id)

    async def _send_post(self):
        text = await self.__form.menu_send_advertiser(message_text=self.__text)
        await bot.send_message(chat_id=self.__user_id, text=text,  reply_markup=await self.__inline.menu_send_blogger(),
                               disable_web_page_preview=True)


class NewMessage(StatesGroup):

    @staticmethod
    async def menu_answer_message_from_advertiser(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"])
            text = call.message.html_text + f"\n\n{Lang.newOrder.advertiser.sendMessage}"
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=text, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_back_send_blogger())

    @staticmethod
    async def menu_answer_message_back_from_advertiser(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"])
            text = call.message.html_text.split(f"\n\n{Lang.newOrder.advertiser.sendMessage}")[0]
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=text, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_send_blogger())

    @staticmethod
    async def menu_answer_message_from_blogger(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"])
            text = call.message.html_text + f"\n\n{Lang.newOrder.advertiser.sendMessage}"
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=text, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_back_send_advertiser())

    @staticmethod
    async def menu_answer_message_back_from_blogger(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"])
            text = call.message.html_text.split(f"\n\n{Lang.newOrder.advertiser.sendMessage}")[0]
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=text, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_send_advertiser())

    async def menu_send_message(self, message: types.Message, state: FSMContext):
        print(1)
        try:
            async with state.proxy() as data:
                Callback = message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data.split("_")
                blogger_area_id = int(message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data.split("_")[1])
                status, json = await self._project_blogger(blogger_area_id, data)
                Lang: Model = Txt.language[data.get('lang')]
                if Callback[0] == "BackNewMessageFromAdvertiser" or Callback[0] == "BackMessageFromAdvertiser":
                    send = SendMessageAdvertiser(data=json, text=message.html_text, blogger_area_id=blogger_area_id)
                    await send.answer()
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.reply_to_message.message_id,
                                                text=Lang.newOrder.blogger.end)
                elif Callback[0] == "BackNewMessageFromBlogger":
                    send = SendMessageBlogger(data=json, text=message.html_text, blogger_area_id=blogger_area_id)
                    await send.answer()
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.reply_to_message.message_id,
                                                text=Lang.newOrder.advertiser.end)
        except Exception as ex:
            pass

    @staticmethod
    async def menu_answer_message_advertiser(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"])
            text = call.message.html_text + f"\n\n{Lang.newOrder.advertiser.sendMessage}"
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=text, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_back_send_blogger2())

    async def menu_answer_message_back_advertiser(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["blogger_area_id"] = int(call.data.split("_")[1])
            Lang: Model = Txt.language[data.get('lang')]
            status, json = await self._project_blogger(data["blogger_area_id"], data)
            inline = InlinePostBlogger(language=data.get('lang'), blogger_area_id=data["blogger_area_id"],
                                       order_id=json.get("order_id"))
            text = call.message.html_text.split(f"\n\n{Lang.newOrder.advertiser.sendMessage}")[0]
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            parse_mode="html", text=text, disable_web_page_preview=True,
                                            reply_markup=await inline.menu_accept())

    @staticmethod
    async def _project_blogger(blogger_area_id, data):
        status, json = await fastapi.project_blogger(blogger_area_id=blogger_area_id, token=data.get("token"))
        return status, json

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_answer_message_from_advertiser,
                                           lambda x: x.data.startswith("NewMessageFromAdvertiser"),                     state="*")
        dp.register_callback_query_handler(self.menu_answer_message_back_from_advertiser,
                                           lambda x: x.data.startswith("BackNewMessageFromAdvertiser"),                 state="*")
        dp.register_callback_query_handler(self.menu_answer_message_from_blogger,
                                           lambda x: x.data.startswith("NewMessageFromBlogger"),                        state="*")
        dp.register_callback_query_handler(self.menu_answer_message_back_from_blogger,
                                           lambda x: x.data.startswith("BackNewMessageFromBlogger"),                    state="*")
        dp.register_message_handler(self.menu_send_message, IsReplyFilter(is_reply=True),
                                    content_types=["text"],                                                             state="*")
        dp.register_callback_query_handler(self.menu_answer_message_advertiser,
                                           lambda x: x.data.startswith("MessageFromAdvertiser"),                        state="*")
        dp.register_callback_query_handler(self.menu_answer_message_back_advertiser,
                                           lambda x: x.data.startswith("BackMessageFromAdvertiser"),                    state="*")
