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
from text.common.formIndividualData import FormIndividualData
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class AddDataIndividualAdvertiser(StatesGroup):
    addData_level1 = State()
    addData_level2 = State()

    title_level1 = State()
    legalAddress_level1 = State()
    pinfl_level1 = State()
    paymentAccount_level1 = State()
    bank_level1 = State()
    mfo_level1 = State()
    phone_level1 = State()

    # menu_add_data
    async def menu_add_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.addData_level1.set()
        async with state.proxy() as data:
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
        if data.get('new_individual') is None:
            data["new_individual"] = {}

    # menu_change_data
    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._change_data(message, data)

    async def _change_data(self, message, data):
        await self.addData_level2.set()
        inline, reply, Lang, form = await self._prepare(data)
        await self._change(message, data, inline, form)

    @staticmethod
    async def _prepare(data):
        reply = ReplyUser(language=data.get('lang'))
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormIndividualData(data=data.get("new_individual"), language=data.get('lang'), email=data.get("email"))
        return inline, reply, Lang, form

    @staticmethod
    async def _change(message, data, inline, form):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_individual())
        data['message_id'] = message1.message_id

    # menu_title
    async def menu_title(self, call: types.CallbackQuery, state: FSMContext):
        await self.title_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataTitleIndividual,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_title
    async def menu_get_title(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get('new_individual')["title"] = message.text
            await self._change_data(message, data)

    # menu_legal_address
    async def menu_legal_address(self, call: types.CallbackQuery, state: FSMContext):
        await self.legalAddress_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id,
                                        text=Lang.personalData.common.newDataLegalAddress,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_legal_address
    async def menu_get_legal_address(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get('new_individual')["legalAddress"] = message.text
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
    async def menu_get_pinfl(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get('new_individual')["pinfl"] = message.text
            await self._change_data(message, data)

    # menu_payment_account
    async def menu_payment_account(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentAccount_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id,
                                        text=Lang.personalData.common.newDataPaymentAccount,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_payment_account
    async def menu_get_payment_account(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get('new_individual')["paymentAccount"] = message.text
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
    async def menu_get_bank(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get('new_individual')["bank"] = message.text
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
    async def menu_get_mfo(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get('new_individual')["mfo"] = message.text
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
    async def menu_get_phone(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            phone = phonenumbers.parse("+" + message.text)
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            data.get('new_individual')["phone"] = phone
            await self._change_data(message, data)

    # menu_end
    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            if await self._check_data(call, data):
                await state.set_state("MenuAdvertiser:menuAdvertiser_level1")

    @staticmethod
    async def _prepare_end(data):
        Lang: Model = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        return Lang, reply

    async def _check_data(self, call, data):
        Lang, reply = await self._prepare_end(data)
        if len(data.get("new_individual")) != 7:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
            return False
        else:
            await self._end(call, data, Lang, reply)
            await self._add_entity(data)
            data.pop("new_entity")
            data.pop("new_individual")
            data.pop("new_selfEmployedCard")
            data.pop("new_selfEmployedAccount")
            return True

    @staticmethod
    async def _end(call, data, Lang, reply):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        await bot.send_message(chat_id=call.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _add_entity(data):
        json = await func.add_individual(data=data.get("new_individual"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    def register_handlers_personal(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_add_data, text="individual",                                       state="PersonalDataAdvertiser:personalDataAdvertiser_level2")
        dp.register_callback_query_handler(self.menu_add_data, text="back",                                             state=self.addData_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.addData_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back", state=[self.title_level1,
                                                                                      self.legalAddress_level1,
                                                                                      self.pinfl_level1,
                                                                                      self.paymentAccount_level1,
                                                                                      self.bank_level1,
                                                                                      self.mfo_level1,
                                                                                      self.phone_level1])

        dp.register_callback_query_handler(self.menu_title, text="title",                                               state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_legal_address, text="legalAddress",                                state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                                   state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_payment_account,                                                   text="paymentAccount", state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.addData_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.addData_level2)

        dp.register_message_handler(self.menu_get_title, IsTitle(), content_types="text",                               state=self.title_level1)
        dp.register_message_handler(self.menu_get_legal_address, IsLegalAddress(), content_types="text",                state=self.legalAddress_level1)
        dp.register_message_handler(self.menu_get_pinfl, IsPinfl(), content_types="text",                                   state=self.pinfl_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.addData_level1)

