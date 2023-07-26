from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import *

from config import bot
from handlers.advertiser.menu import MenuAdvertiser
from handlers.advertiser.registration.exist_account import ExistAdvertiser
from handlers.advertiser.registration.registration import RegistrationAdvertiser
from handlers.blogger.menu import MenuBlogger
from handlers.blogger.registration.exist_account import ExistBlogger
from handlers.blogger.registration.registration import RegistrationBlogger
from keyboards.inline.common.common import Start
from keyboards.inline.common.registration import InlineRegistration
from keyboards.reply.common.common import ReplyStart
from keyboards.reply.common.user import ReplyUser
from looping import pg, fastapi
from model.user import User
from text.common.formCommon import FormCommon
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class MenuCommon(StatesGroup):
    start = State()

    async def void(self, call: types.CallbackQuery):
        await call.answer()

    async def command_start(self, message: types.Message, state: FSMContext):
        print(1)
        async with state.proxy() as data:
            await self._get_token(data=data)
            data['lang'] = await pg.select_language(user_id=message.from_user.id)
            new_data = User(lang=data.get("lang"), email=data.get("email"), password=data.get("password"), token=data.get("token"))
            await self._check_user_exist(message=message, data=data)
        await state.set_data(data=new_data)

    async def _check_user_exist(self, message, data):
        self.__exist = await pg.exist_telegram_user(user_id=message.from_user.id)
        exist_lang = await pg.exist_lang(user_id=message.from_user.id)
        if self.__exist is True and exist_lang is True:
            await self._user(message=message, data=data)
        elif self.__exist is False or exist_lang is False:
            await self._new_user(message=message)

    async def _user(self, message, data):
        await pg.block_status(user_id=message.from_user.id, status=True)
        await self._check_role(message=message, data=data)

    async def _new_user(self, message):
        await self.start.set()
        start = Start()
        await bot.send_message(chat_id=message.from_user.id, text=Txt.choose_language,
                               reply_markup=await start.choose_language())
        if self.__exist is False:
            await self._record(message=message)

    @staticmethod
    async def _record(message):
        user_id = message.from_user.id
        username = message.from_user.username
        await pg.first_rec_telegram_user(user_id=user_id, username=username)

    async def _check_role(self,  message, data):
        await self._check_email(message=message, data=data)
        await self._role(message=message, data=data)

    async def _check_email(self, message, data):
        data["email"] = await pg.select_email(user_id=message.from_user.id)
        if data.get("email") is not None:
            await self._get_role(data=data)

    @staticmethod
    async def _get_role(data):
        status, exist = await fastapi.exist_user(email=data.get("email"))
        data["role"] = exist.get("role")

    async def _role(self, message, data):
        if data.get("role") is None or data.get("password") is None or data.get("email") is None:
            await self._no_name(message=message, data=data)
        elif data.get("role") == "blogger":
            await self._get_token(data=data)
            await self._start_blogger(message=message, data=data)
        elif data.get("role") == "advertiser":
            await self._get_token(data=data)
            await self._start_advertiser(message=message, data=data)

    @staticmethod
    async def _get_token(data):
        user = User(username=data.get("email"), password=data.get("password"))
        data['token'] = await fastapi.get_token(user=user)

    async def _start_blogger(self, message, data):
        await self._greeting_blogger(message=message, data=data)
        await MenuBlogger.menuBlogger_level1.set()

    async def _start_advertiser(self, message, data):
        await self._greeting_advertiser(message=message, data=data)
        await MenuAdvertiser.menuAdvertiser_level1.set()

    async def _no_name(self, message, data):
        await self._greeting_no_name(message=message, data=data)
        await self.start.set()

    @staticmethod
    async def _prepare(data, message):
        data['lang'] = await pg.select_language(user_id=message.from_user.id)
        Lang: Model = Txt.language[data.get('lang')]
        return Lang

    async def _greeting_blogger(self, message, data):
        Lang = await self._prepare(message=message, data=data)
        reply = ReplyUser(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.menu_blogger())

    async def _greeting_no_name(self, message, data):
        Lang = await self._prepare(message=message, data=data)
        reply = ReplyStart(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.start())

    async def _greeting_advertiser(self,  message, data):
        Lang = await self._prepare(message=message, data=data)
        reply = ReplyUser(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    async def menu_choose_language(self, call: types.callback_query, state: FSMContext):
        async with state.proxy() as data:
            data['lang'] = call.data
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyStart(language=data.get('lang'))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await pg.update_language(language=data.get('lang'), user_id=call.from_user.id)
        await bot.send_message(chat_id=call.message.chat.id, text=Lang.start.start, reply_markup=await reply.start())
        await self.start.set()

    # settings
    @staticmethod
    async def menu_setting(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyStart(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.start.language,
                                   reply_markup=await reply.setting())

    async def menu_change_language(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['lang'] = await self._change_language(message)
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyStart(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.menu,
                                   reply_markup=await reply.start())

    @staticmethod
    async def _change_language(message):
        new_language = message.text
        user_id = message.from_user.id
        if new_language == Txt.settings.rus:
            language = Txt.rus_var
        elif new_language == Txt.settings.uzb:
            language = Txt.uzb_var
        else:
            return Txt.uzb_var
        await pg.update_language(language=language, user_id=user_id)
        return language

    async def main_menu(self, message: types.Message, state: FSMContext):
        await self.start.set()
        async with state.proxy() as data:
            await state.set_data(data={"lang": data.get('lang')})
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyStart(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.menu,
                                   reply_markup=await reply.start())

    async def registration_blogger(self, message: types.Message, state: FSMContext):
        await state.set_state("RegistrationBlogger:regBlogger_level1")
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlineRegistration(language=data.get('lang'))
            reply = ReplyUser(language=data.get('lang'))
            form = FormCommon(language=data.get("lang"))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.start.blogger,
                                   reply_markup=await reply.main_menu())
            message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_rules(),
                                              reply_markup=await inline.menu_agreement(), disable_web_page_preview=True)
            data['message_id'] = message1.message_id

    async def registration_advertiser(self, message: types.Message, state: FSMContext):
        await state.set_state("RegistrationAdvertiser:regAdvertiser_level0")
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.registration.advertiser.about,
                                   reply_markup=await reply.menu_start())
            data['message_id'] = message1.message_id


    # register_handler
    def register_handlers_menu_common(self, dp: Dispatcher):
        dp.register_message_handler(self.command_start, commands="start",                                               state='*')

        dp.register_callback_query_handler(self.void, text='void',                                                      state="*")
        dp.register_callback_query_handler(self.menu_choose_language, text=Txt.language.keys(),                         state=self.start)

        dp.register_message_handler(self.main_menu, text=Txt.menu.menu,                                                 state=[self.start,
                                                                                                                               *ExistBlogger.states_names,
                                                                                                                               *ExistAdvertiser.states_names,
                                                                                                                               *(RegistrationBlogger.states_names[:-1]),
                                                                                                                               *(RegistrationAdvertiser.states_names[:-1])])
        dp.register_message_handler(self.registration_blogger, text=Txt.start.blogger,                                  state=self.start)
        dp.register_message_handler(self.registration_advertiser, text=Txt.start.advertiser,                            state=self.start)

        dp.register_message_handler(self.menu_setting, text=Txt.menu.lang,                                              state=self.start)
        dp.register_message_handler(self.menu_change_language, text=Txt.settings.language,                              state=self.start)
