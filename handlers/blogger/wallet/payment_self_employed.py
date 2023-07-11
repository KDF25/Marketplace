from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from keyboards.inline.common.personal_data import InlinePersonalData
from looping import fastapi
from model.wallet import WalletModel
from text.common.formSelfEmployedAccountData import FormSelfEmployedAccountData
from text.language.main import Text_main
from filters.personal_data import IsFio, IsNumber, IsDate, IsPaymentAccount, IsBank, IsMfo, IsPhone, IsPinfl
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class PaymentSelfEmployedAccountBlogger(StatesGroup):

    payment_level1 = State()
    payment_level2 = State()

    fio_level1 = State()
    number_level1 = State()
    date_level1 = State()
    pinfl_level1 = State()
    paymentAccount_level1 = State()
    bank_level1 = State()
    mfo_level1 = State()
    phone_level1 = State()

    # menu_personal_data
    async def menu_personal_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.payment_level1.set()
        async with state.proxy() as data:
            await self._callback_data(data=data)
            Lang, inline, form = await self._prepare(data=data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_personal_data(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_first_data())
            # print(data)

    @staticmethod
    async def _callback_data(data):
        if data.get("selfEmployedAccount") is None:
            data["selfEmployedAccount"] = {}
        data.get("selfEmployedAccount")["cash"] = data.get("cash")

    # menu_change_data
    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._change_data(message, data)

    async def _change_data(self, message, data):
        await self.payment_level2.set()
        Lang, inline, form = await self._prepare(data)
        await self._change(message, inline, form, data)

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormSelfEmployedAccountData(data=data.get("selfEmployedAccount"), language=data.get('lang'), email=data.get("email"))
        return Lang, inline, form

    @staticmethod
    async def _change(message: Union[types.Message, types.CallbackQuery], inline, form, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_self_employed_account())
        data['message_id'] = message1.message_id

    async def menu_fio(self, call: types.CallbackQuery, state: FSMContext):
        await self.fio_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataFio,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_fio(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["fio"] = message.text
            await self._change_data(message, data)

    async def menu_number(self, call: types.CallbackQuery, state: FSMContext):
        await self.number_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataNumber,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_number(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["number"] = message.text
            await self._change_data(message, data)

    async def menu_date(self, call: types.CallbackQuery, state: FSMContext):
        await self.date_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataDate,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_date(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["date"] = message.text
            await self._change_data(message, data)

    async def menu_pinfl(self, call: types.CallbackQuery, state: FSMContext):
        await self.pinfl_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPinfl,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_pinfl(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["pinfl"] = message.text
            await self._change_data(message, data)

    async def menu_payment_account(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentAccount_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPaymentAccount,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_payment_account(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["paymentAccount"] = message.text
            await self._change_data(message, data)

    async def menu_bank(self, call: types.CallbackQuery, state: FSMContext):
        await self.bank_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataBank,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_bank(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["bank"] = message.text
            await self._change_data(message, data)

    async def menu_mfo(self, call: types.CallbackQuery, state: FSMContext):
        await self.mfo_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataMfo,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_mfo(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["mfo"] = message.text
            await self._change_data(message, data)

    async def menu_phone(self, call: types.CallbackQuery, state: FSMContext):
        await self.phone_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPhone,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_phone(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedAccount")["phone"] = message.text
            await self._change_data(message, data)

    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_data(call=call, data=data)

    async def _check_data(self, call, data):
        Lang, inline, form = await self._prepare(data=data)
        if len(data.get("selfEmployedAccount")) != 9:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
        else:
            await self._end(call=call, form=form)
            await self._add_self_employed(data=data)
            await self._payment_didox(data=data)
            data.pop("entity")
            data.pop("individual")
            data.pop("selfEmployedAccount")
            data.pop("selfEmployedCard")

    @staticmethod
    async def _end(call, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_payment(),
                                        message_id=call.message.message_id)

    @staticmethod
    async def _add_self_employed(data):
        json = await func.add_self_employed_account(data=data.get("selfEmployedAccount"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    @staticmethod
    async def _payment_didox(data):
        json = WalletModel(type_legal="self_employed", amount=data.get("selfEmployedAccount").get("cash"))
        await fastapi.payment_didox(json=json, token=data.get('token'))

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_personal_data, text="emp",                                         state="PaymentCommonBlogger:paymentCommon_level3")
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=self.payment_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.payment_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back",                                          state=[self.fio_level1,
                                                                                                                               self.number_level1,
                                                                                                                               self.date_level1,
                                                                                                                               self.pinfl_level1,
                                                                                                                               self.paymentAccount_level1,
                                                                                                                               self.bank_level1,
                                                                                                                               self.mfo_level1,
                                                                                                                               self.phone_level1])

        dp.register_callback_query_handler(self.menu_fio, text="fio",                                                   state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_number, text="number",                                             state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_date, text="date",                                                 state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                                   state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.payment_level2)

        dp.register_message_handler(self.menu_get_fio, IsFio(), content_types="text",                                   state=self.fio_level1)
        dp.register_message_handler(self.menu_get_number, IsNumber(), content_types="text",                             state=self.number_level1)
        dp.register_message_handler(self.menu_get_date, IsDate(), content_types="text",                                 state=self.date_level1)
        dp.register_message_handler(self.menu_get_pinfl, IsPinfl(), content_types="text",                               state=self.pinfl_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.payment_level1)

