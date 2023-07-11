import asyncio
from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from keyboards.inline.blogger.platform import InlinePlatformBlogger
from keyboards.inline.common.registration import InlineRegistration
from looping import pg, fastapi
from text.common.formCommon import FormCommon
from text.common.formRegistration import FormRegistration
from text.language.main import Text_main
from model.user import User, Code
from filters.registration import IsEmail, IsCode, IsPassword, IsNew

Txt = Text_main()


class RegistrationBlogger(StatesGroup):

    regBlogger_level1 = State()
    regBlogger_level2 = State()
    regBlogger_level3 = State()
    regBlogger_level4 = State()
    regBlogger_level5 = State()


    async def menu_start(self, call: types.CallbackQuery, state: FSMContext):
        await self.regBlogger_level1.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare(data)
            form = FormCommon(language=data.get("lang"))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_rules(),
                                        reply_markup=await inline.menu_agreement(), message_id=call.message.message_id,
                                        disable_web_page_preview=True)

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlineRegistration(language=data.get('lang'))
        return Lang, inline

    async def menu_login(self, call: types.CallbackQuery, state: FSMContext):
        await self.regBlogger_level2.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare(data)
            data['message_id'] = call.message.message_id
            data["countdown"] = False
            if call.data == "agree":
                with suppress(MessageNotModified, MessageToEditNotFound):
                    await call.answer()
                    await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.registration.common.login,
                                                message_id=call.message.message_id, reply_markup=await inline.menu_login())
            else:
                with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
                message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.registration.common.login,
                                                  reply_markup=await inline.menu_login())
                data["message_id"] = message1.message_id

    async def menu_code(self, message: types.Message, state: FSMContext):
        await self.regBlogger_level3.set()
        async with state.proxy() as data:
            data['email'] = message.text
            data["countdown"] = True
            form, inline = await self._prepare_code(data)
            await self._code(message, data, form, inline)
        await self._send_code(data)
        await self._start_countdown(start=57, message=message, data=data)

    @staticmethod
    async def _prepare_code(data):
        form = FormRegistration(data=data)
        inline = InlineRegistration(language=data.get('lang'))
        return form, inline

    @staticmethod
    async def _code(message, data, form, inline):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_code(),
                                          reply_markup=await inline.menu_code(second=60))
        data["message_id1"] = message1.message_id

    @staticmethod
    async def _send_code(data):
        await fastapi.send_code(email=data.get("email"))

    async def _start_countdown(self, start: int, message, data):
        form, inline = await self._prepare_code(data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            for second in range(start, -3, -3):
                if data.get('countdown') is False:
                    break
                elif second >= 3:
                    await self._countdown(second, message, data, form, inline)
                elif second == 0:
                    await self._end_countdown(message, data, form, inline)

    @staticmethod
    async def _countdown(second: int, message, data, form, inline):
        await bot.edit_message_text(chat_id=message.from_user.id, text=await form.menu_code(),
                                    message_id=data.get('message_id1'),
                                    reply_markup=await inline.menu_code(second=second))
        await asyncio.sleep(3)

    @staticmethod
    async def _end_countdown(message, data, form, inline):
        await bot.edit_message_text(chat_id=message.from_user.id, text=await form.menu_code(),
                                    message_id=data.get('message_id1'), reply_markup=await inline.menu_resend())

    async def menu_resend_code(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            form, inline = await self._prepare_code(data)
            await self._countdown(second=60, message=call, data=data, form=form, inline=inline)
            await self._send_code(data)
        await self._start_countdown(start=57, message=call, data=data)

    async def menu_password(self, message: types.Message, state: FSMContext):
        message = message
        async with state.proxy() as data:
            data["code"] = message.text
            await self._check_code(message, data)

    async def _check_code(self, message, data):
        code = Code(email=data.get("email"), code=data.get("code"))
        status = await fastapi.check_code(code=code)
        await self._check_status_code(status, message, data)

    async def _check_status_code(self, status, message, data):
        Lang, inline = await self._prepare(data)
        if status == 200:
            await self._success_code(message, data, Lang, inline)
        elif status == 400:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.invalidCode)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.error)

    async def _success_code(self, message, data, Lang, inline):
        await self.regBlogger_level4.set()
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id1'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.registration.common.password,
                                          reply_markup=await inline.menu_back())
        data['message_id'] = message1.message_id

    async def menu_registration(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['password'] = message.text
            await self._rec_blogger(message, data)

    @staticmethod
    async def _prepare_rec(data):
        Lang = Txt.language[data.get('lang')]
        inline_rec = InlinePlatformBlogger(language=data.get('lang'))
        return Lang, inline_rec

    async def _rec_blogger(self, message, data):
        user = User(email=data.get('email'), password_hash=data.get("password"), role="blogger",
                    wallet=0, code=data.get("code"))
        status, json = await fastapi.create_user(user=user)
        await self._check_status_rec(message, data, status, json)

    async def _check_status_rec(self, message, data, status, json):
        Lang, inline_rec = await self._prepare_rec(data)
        if status == 201:
            await self._get_token(data)
            await self._success_rec(message, data, json, Lang, inline_rec)
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.error)

    async def _success_rec(self, message, data, json, Lang, inline_rec):
        await self.regBlogger_level5.set()
        await pg.update_telegram_user(user_id=message.from_user.id, email=data.get('email'),
                                      client_id=json.get("id"))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.registration.common.blogger,
                                          reply_markup=await inline_rec.menu_add())
        data['message_id'] = message1.message_id

    @staticmethod
    async def _get_token(data):
        user = User(username=data.get("email"), password=data.get("password"))
        data['token'] = await fastapi.get_token(user=user)

    def register_handlers_registration_blogger(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_start, text="back",                                                state=self.regBlogger_level2)

        dp.register_callback_query_handler(self.menu_login, text="agree",                                               state=self.regBlogger_level1)
        dp.register_callback_query_handler(self.menu_login, text="back",                                                state=[self.regBlogger_level3, self.regBlogger_level4, "ExistBlogger:existBlogger_level1"])

        dp.register_message_handler(self.menu_code, IsEmail(), IsNew(), content_types='text',                           state=self.regBlogger_level2)

        dp.register_callback_query_handler(self.menu_resend_code, text='resendCode',                                    state=self.regBlogger_level3)
        dp.register_message_handler(self.menu_password, IsCode(), content_types='text',                                 state=self.regBlogger_level3)
        dp.register_message_handler(self.menu_registration, IsPassword(), content_types='text',                         state=self.regBlogger_level4)


