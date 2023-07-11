from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, \
    MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from text.common.formSelfEmployedCardData import FormSelfEmployedCardData
from text.language.main import Text_main
from filters.personal_data import IsFio, IsNumber, IsDate, IsPaymentAccount, IsBank, IsMfo, IsPhone, IsPinfl, \
    IsCardDate, IsCardNumber
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class AddDataSelfEmployedCardAdvertiser(StatesGroup):
    addData_level1 = State()
    addData_level2 = State()

    fio_level1 = State()
    number_level1 = State()
    date_level1 = State()
    pinfl_level1 = State()
    paymentAccount_level1 = State()
    bank_level1 = State()
    mfo_level1 = State()
    phone_level1 = State()
    cardNumber_level1 = State()
    cardDate_level1 = State()

    # menu_add_data
    async def menu_add_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.addData_level1.set()
        async with state.proxy() as data:
            print(data)
            await self._callback_data(data)
            inline, reply, Lang, form = await self._prepare(data)
            await self._add_data(call, data, inline, reply, Lang, form)

    async def _add_data(self, message, data, inline, reply, Lang, form):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.account,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(message, data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_personal_data(),
                                          reply_markup=await inline.menu_first_data())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    @staticmethod
    async def _delete_message(message, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id_None'))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))

    @staticmethod
    async def _callback_data(data):
        if data.get('new_selfEmployedCard') is None:
            data["new_selfEmployedCard"] = {}

    # menu_change_data
    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            print(data)
            await self._change_data(message, data)

    async def _change_data(self, message, data):
        await self.addData_level2.set()
        inline, reply, Lang, form = await self._prepare(data)
        await self._change(message, data, inline, form)

    @staticmethod
    async def _prepare(data):
        reply = ReplyUser(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormSelfEmployedCardData(data=data.get("new_selfEmployedCard"), language=data.get('lang'),
                                    email=data.get("email"))
        return inline, reply, Lang, form

    @staticmethod
    async def _change(message, data, inline, form):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_self_employed_card())
        data['message_id'] = message1.message_id

    # menu_fio
    async def menu_fio(self, call: types.CallbackQuery, state: FSMContext):
        await self.fio_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataFioCard,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_fio
    async def menu_get_fio(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["fio"] = message.text
            await self._change_data(message, data)

    # menu_number
    async def menu_number(self, call: types.CallbackQuery, state: FSMContext):
        await self.number_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataNumber,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_number
    async def menu_get_number(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["number"] = message.text
            await self._change_data(message, data)

    # menu_date
    async def menu_date(self, call: types.CallbackQuery, state: FSMContext):
        await self.date_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataDate,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_date
    async def menu_get_date(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["date"] = message.text
            await self._change_data(message, data)

    # menu_pinfl
    async def menu_pinfl(self, call: types.CallbackQuery, state: FSMContext):
        await self.pinfl_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPinfl,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_pinfl
    async def menu_get_pinfl(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["pinfl"] = message.text
            await self._change_data(message, data)

    # menu_payment_account
    async def menu_payment_account(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentAccount_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPaymentAccount,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_payment_account
    async def menu_get_payment_account(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["paymentAccount"] = message.text
            await self._change_data(message, data)

    # menu_bank
    async def menu_bank(self, call: types.CallbackQuery, state: FSMContext):
        await self.bank_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataBank,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_bank
    async def menu_get_bank(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["bank"] = message.text
            await self._change_data(message, data)

    # menu_mfo
    async def menu_mfo(self, call: types.CallbackQuery, state: FSMContext):
        await self.mfo_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataMfo,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_mfo
    async def menu_get_mfo(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["mfo"] = message.text
            await self._change_data(message, data)

    # menu_phone
    async def menu_phone(self, call: types.CallbackQuery, state: FSMContext):
        await self.phone_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPhone,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_phone
    async def menu_get_phone(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["phone"] = message.text
            await self._change_data(message, data)

    # menu_card_number
    async def menu_card_number(self, call: types.CallbackQuery, state: FSMContext):
        await self.cardNumber_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataCardNumber,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_card_number
    async def menu_get_card_number(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["cardNumber"] = message.text
            await self._change_data(message, data)

    # menu_card_date
    async def menu_card_date(self, call: types.CallbackQuery, state: FSMContext):
        await self.cardDate_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataCardDate,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_card_number
    async def menu_get_card_date(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            print(data)
            data.get("new_selfEmployedCard")["cardDate"] = message.text
            await self._change_data(message, data)

    # menu_end
    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            if await self._check_data(call, data):
                await state.set_state("MenuAdvertiser:menuAdvertiser_level1")

    @staticmethod
    async def _prepare_end(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        return Lang, reply

    async def _check_data(self, call, data):
        Lang, reply = await self._prepare_end(data)
        if len(data.get("new_selfEmployedCard")) != 10:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
            return False
        else:
            await self._end(call, data, Lang, reply)
            await self._add_self_employed(data)
            data.pop("new_entity")
            data.pop("new_individual")
            data.pop("new_selfEmployedCard")
            data.pop("new_selfEmployedCard")
            return True

    @staticmethod
    async def _end(call, data, Lang, reply):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        await bot.send_message(chat_id=call.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _add_self_employed(data):
        json = await func.add_self_employed_card(data=data.get("new_selfEmployedCard"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_add_data, text="selfEmployedCard",                                 state="PersonalDataAdvertiser:personalDataAdvertiser_level2")
        dp.register_callback_query_handler(self.menu_add_data, text="back",                                             state=self.addData_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.addData_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back", state=[self.fio_level1,
                                                                                      self.number_level1,
                                                                                      self.date_level1,
                                                                                      self.pinfl_level1,
                                                                                      self.paymentAccount_level1,
                                                                                      self.bank_level1,
                                                                                      self.mfo_level1,
                                                                                      self.cardNumber_level1,
                                                                                      self.cardDate_level1])

        dp.register_callback_query_handler(self.menu_fio, text="fio",                                                   state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_number, text="number",                                             state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_date, text="date",                                                 state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                               state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_card_number, text="cardNumber",                                    state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_card_date, text="cardDate",                                        state=self.addData_level2)

        dp.register_message_handler(self.menu_get_fio, IsFio(), content_types="text",                                   state=self.fio_level1)
        dp.register_message_handler(self.menu_get_number, IsNumber(), content_types="text",                             state=self.number_level1)
        dp.register_message_handler(self.menu_get_date, IsDate(), content_types="text",                                 state=self.date_level1)
        dp.register_message_handler(self.menu_get_pinfl, IsPinfl(), content_types="text",                               state=self.pinfl_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)
        dp.register_message_handler(self.menu_get_card_number, IsCardNumber(), content_types="text",                    state=self.cardNumber_level1)
        dp.register_message_handler(self.menu_get_card_date, IsCardDate(), content_types="text",                        state=self.cardDate_level1)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.addData_level1)



