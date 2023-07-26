from contextlib import suppress
from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import *

from filters.personal_data import *
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from text.common.formSelfEmployedAccountData import FormSelfEmployedAccountData
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FirstSelfEmployedAccountBlogger(StatesGroup):

    firstData_level1 = State()
    firstData_level2 = State()

    fio_level1 = State()
    number_level1 = State()
    date_level1 = State()
    pinfl_level1 = State()
    paymentAccount_level1 = State()
    bank_level1 = State()
    mfo_level1 = State()
    phone_level1 = State()

    # menu_first_data
    async def menu_first_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.firstData_level1.set()
        async with state.proxy() as data:
            await self._callback_data(data)
            Lang, inline, form = await self._prepare(data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_personal_data(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_first_data())

    @staticmethod
    async def _callback_data(data):
        if data.get("selfEmployedAccount") is None:
            data["selfEmployedAccount"] = {}

    # menu_change_data
    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._change_data(message, data)

    async def _change_data(self, message, data):
        await self.firstData_level2.set()
        Lang, inline, form = await self._prepare(data)
        await self._change(message, data, inline, form)

    @staticmethod
    async def _prepare(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormSelfEmployedAccountData(data=data.get("selfEmployedAccount"), language=data.get('lang'), email=data.get("email"))
        return Lang, inline, form

    @staticmethod
    async def _change(message, data, inline, form):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_self_employed_account())
        data['message_id'] = message1.message_id

    # menu_fio
    async def menu_fio(self, call: types.CallbackQuery, state: FSMContext):
        await self.fio_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataFio,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_fio
    async def menu_get_fio(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["fio"] = message.text
            await self._change_data(message, data)

    # menu_number
    async def menu_number(self, call: types.CallbackQuery, state: FSMContext):
        await self.number_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataNumber,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_number
    async def menu_get_number(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["number"] = message.text
            await self._change_data(message, data)

    # menu_date
    async def menu_date(self, call: types.CallbackQuery, state: FSMContext):
        await self.date_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataDate,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_date
    async def menu_get_date(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["date"] = message.text
            await self._change_data(message, data)

    # menu_pinfl
    async def menu_pinfl(self, call: types.CallbackQuery, state: FSMContext):
        await self.pinfl_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPinfl,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_pinfl
    async def menu_get_pinfl(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["pinfl"] = message.text
            await self._change_data(message, data)

    # menu_payment_account
    async def menu_payment_account(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentAccount_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPaymentAccount,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_payment_account
    async def menu_get_payment_account(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["paymentAccount"] = message.text
            await self._change_data(message, data)

    # menu_bank
    async def menu_bank(self, call: types.CallbackQuery, state: FSMContext):
        await self.bank_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataBank,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_bank
    async def menu_get_bank(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["bank"] = message.text
            await self._change_data(message, data)

    # menu_mfo
    async def menu_mfo(self, call: types.CallbackQuery, state: FSMContext):
        await self.mfo_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataMfo,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_mfo
    async def menu_get_mfo(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["mfo"] = message.text
            await self._change_data(message, data)

    # menu_phone
    async def menu_phone(self, call: types.CallbackQuery, state: FSMContext):
        await self.phone_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPhone,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_phone
    async def menu_get_phone(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["phone"] = message.text
            await self._change_data(message, data)

    # menu_end
    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            if await self._check_data(call, data):
                await state.set_state("MenuBlogger:menuBlogger_level1")

    @staticmethod
    async def _prepare_end(data):
        Lang: Model = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        return Lang, reply

    async def _check_data(self, call, data):
        Lang, reply = await self._prepare_end(data)
        if len(data.get("selfEmployedAccount")) != 8:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
            return False
        else:
            await self._end(call, data, Lang, reply)
            await self._add_self_employed(data)
            data.pop("selfEmployedAccount")
            return True

    @staticmethod
    async def _end(call, data, Lang, reply):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        await bot.send_message(chat_id=call.from_user.id, text=Lang.personalData.common.moderation,
                               reply_markup=await reply.menu_blogger())

    @staticmethod
    async def _add_self_employed(data):
        json = await func.add_self_employed_account(data=data.get("selfEmployedAccount"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_first_data, text="selfEmployedAccount",                            state="FirstPlatformBlogger:firstPlatform_level15")
        dp.register_callback_query_handler(self.menu_first_data, text="back",                                           state=self.firstData_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.firstData_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back",                                          state=[self.fio_level1,
                                                                                                                               self.number_level1,
                                                                                                                               self.date_level1,
                                                                                                                               self.pinfl_level1,
                                                                                                                               self.paymentAccount_level1,
                                                                                                                               self.bank_level1,
                                                                                                                               self.mfo_level1,
                                                                                                                               self.phone_level1])

        dp.register_callback_query_handler(self.menu_fio, text="fio",                                                   state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_number, text="number",                                             state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_date, text="date",                                                 state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                                   state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.firstData_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.firstData_level2)

        dp.register_message_handler(self.menu_get_fio, IsFio(), content_types="text",                                   state=self.fio_level1)
        dp.register_message_handler(self.menu_get_number, IsNumber(), content_types="text",                             state=self.number_level1)
        dp.register_message_handler(self.menu_get_date, IsDate(), content_types="text",                                 state=self.date_level1)
        dp.register_message_handler(self.menu_get_pinfl, IsPinfl(), content_types="text",                               state=self.pinfl_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.firstData_level1)

