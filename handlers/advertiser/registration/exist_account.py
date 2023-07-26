import asyncio
from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import *

from config import bot
from filters.registration import IsEmail, IsCode, IsPassword, HaveAccount, IsExist
from handlers.advertiser.menu import MenuAdvertiser
from keyboards.inline.common.registration import InlineRegistration
from keyboards.reply.common.user import ReplyUser
from looping import fastapi, pg
from text.common.formExist import FormExist
from text.language.main import Text_main
from text.language.ru import Ru_language as Model
from model.user import Code, User

Txt = Text_main()


class ExistAdvertiser(StatesGroup):

    existAdvertiser_level1 = State()
    existAdvertiser_level2 = State()
    existAdvertiser_level3 = State()
    existAdvertiser_level4 = State()

    @staticmethod
    async def _prepare(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlineRegistration(language=data.get('lang'))
        return Lang, inline
        
    async def menu_have_account(self, call: types.CallbackQuery, state: FSMContext):
        await self.existAdvertiser_level1.set()
        async with state.proxy() as data:
            data['message_id'] = call.message.message_id
            Lang, inline = await self._prepare(data=data)
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.registration.existAccount.login,
                                              reply_markup=await inline.menu_back())
            data['message_id'] = message1.message_id

    async def menu_forgot_password(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.existAdvertiser_level2.set()
        async with state.proxy() as data:
            if isinstance(message, types.Message):
                data['email'] = message.text
            Lang, inline = await self._prepare(data=data)
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
            message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.registration.existAccount.password,
                                              reply_markup=await inline.menu_forgot_password())
            data['message_id'] = message1.message_id

    async def menu_code(self, call: types.CallbackQuery, state: FSMContext):
        await self.existAdvertiser_level3.set()
        async with state.proxy() as data:
            form, inline = await self._prepare_code(data)
            await self._countdown(call, data, form, inline, second=60)
            await self._send_code(data)
            await self._start_countdown(call, data, form, inline, second=57)

    @staticmethod
    async def _send_code(data):
        await fastapi.send_code(email=data.get("email"))

    @staticmethod
    async def _prepare_code(data):
        form = FormExist(data=data)
        inline = InlineRegistration(language=data.get('lang'))
        return form, inline

    async def _start_countdown(self,call, data, form, inline, second: int):
        with suppress(MessageNotModified, MessageToEditNotFound):
            for second in range(second, -3, -3):
                if second >= 3:
                    await self._countdown(call, data, form, inline, second=second)
                elif second == 0:
                    await self._end_countdown(call, data, form, inline)

    @staticmethod
    async def _countdown(call, data, form, inline, second: int):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_code(),
                                        message_id=data.get('message_id'), reply_markup=await inline.menu_code(second=second))
            await asyncio.sleep(3)

    @staticmethod
    async def _end_countdown(call, data, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_code(),
                                        message_id=data.get('message_id'), reply_markup=await inline.menu_resend())

    async def menu_resend_code(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            form, inline = await self._prepare_code(data)
            await self._countdown(call, data, form, inline, second=60)
            await self._send_code(data)
        await self._start_countdown(call, data, form, inline, second=57)

    async def menu_password(self, message: types.Message, state: FSMContext):
        message = message
        async with state.proxy() as data:
            data["code"] = message.text
            await self._check_code(message, data)

    async def _check_code(self, message, data,):
        code = Code(email=data.get("email"), code=data.get("code"))
        status = await fastapi.check_code(code=code)
        await self._check_status_code(message, data, status)

    async def _check_status_code(self, message, data, status):
        Lang, inline = await self._prepare(data=data)
        if status == 200:
            await self._success_code(message, data, Lang, inline)
        elif status == 400:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.invalidCode)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.error)

    async def _success_code(self, message, data, Lang, inline):
        await self.existAdvertiser_level4.set()
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, reply_markup=await inline.menu_back(),
                                          text=Lang.registration.existAccount.newPassword)
        data['message_id'] = message1.message_id

    async def menu_main(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["password"] = message.text
            await self._get_token(data)
            Lang, reply = await self._prepare_menu(data)
            if data.get("token").get('errors') is None:
                await self._success_rec(message, data, reply, Lang)
            else:
                await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.invalidPassword)

    async def menu_update_password(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["password"] = message.text
            await self._update_password(message, data)

    @staticmethod
    async def _prepare_menu(data):
        Lang: Model = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        return Lang, reply

    async def _update_password(self, message, data):
        code = Code(email=data.get("email"), password=data.get("password"), code=data.get("code"))
        status = await fastapi.update_password(code=code)
        await self._check_update(message, data, status)

    async def _check_update(self, message, data, status):
        Lang, reply = await self._prepare_menu(data)
        if status == 200:
            await self._get_token(data)
            await self._success_rec(message, data, reply, Lang)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.error)

    async def _success_rec(self, message, data, reply, Lang):
        await self._update_telegram_user(message, data)
        await MenuAdvertiser.menuAdvertiser_level1.set()
        await self._main_menu(message, data, reply, Lang)

    @staticmethod
    async def _main_menu(message, data, reply, Lang):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        await bot.send_message(chat_id=message.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _get_token(data):
        user = User(username=data.get("email"), password=data.get("password"))
        data['token'] = await fastapi.get_token(user=user)

    @staticmethod
    async def _update_telegram_user(message, data):
        status, json = await fastapi.exist_user(email=data.get('email'))
        await pg.update_telegram_user(user_id=message.from_user.id, email=data.get('email'),
                                      client_id=json.get("client_id"))

    def register_handlers_exist_advertiser(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_have_account, HaveAccount(), text="haveAccount",                   state="RegistrationAdvertiser:regAdvertiser_level2")
        dp.register_callback_query_handler(self.menu_have_account, text="back",                                         state=self.existAdvertiser_level2)

        dp.register_message_handler(self.menu_forgot_password,  IsEmail(), IsExist(), content_types='text',             state=self.existAdvertiser_level1)
        dp.register_callback_query_handler(self.menu_forgot_password, text='back',                                      state=self.existAdvertiser_level3)

        dp.register_callback_query_handler(self.menu_code, text='forgotPassword',                                       state=self.existAdvertiser_level2)
        dp.register_callback_query_handler(self.menu_code, text='back',                                                 state=self.existAdvertiser_level4)

        dp.register_callback_query_handler(self.menu_code, text='resendCode',                                           state=self.existAdvertiser_level3)

        dp.register_message_handler(self.menu_password, IsCode(), content_types='text',                                 state=self.existAdvertiser_level3)

        dp.register_message_handler(self.menu_main, content_types='text',                                               state=self.existAdvertiser_level2)
        dp.register_message_handler(self.menu_update_password, IsPassword(), content_types='text',                      state=self.existAdvertiser_level4)
