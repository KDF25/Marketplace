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


class PersonalDataIndividualBlogger(StatesGroup):

    personalData_level1 = State()
    personalData_level2 = State()

    title_level1 = State()
    legalAddress_level1 = State()
    pinfl_level1 = State()
    paymentAccount_level1 = State()
    bank_level1 = State()
    mfo_level1 = State()
    phone_level1 = State()

    # menu_personal_data
    async def menu_personal_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.personalData_level1.set()
        async with state.proxy() as data:
            await self._callback_data(data)
            Lang, inline, form = await self._prepare(data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_personal_data(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_personal_data())

    @staticmethod
    async def _callback_data(data):
        if data.get("individual") is None:
            data["individual"] = {}

    @staticmethod
    async def _prepare(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormIndividualData(data=data.get("individual"), language=data.get('lang'),
                              email=data.get("email"))
        return Lang, inline, form

    # menu_change_data
    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._change_data(message, data)

    async def _change_data(self, message, data):
        await self.personalData_level2.set()
        Lang, inline, form = await self._prepare(data)
        await self._change(message, data, inline, form)

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
    async def menu_get_title(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["title"] = message.text
            await self._change_data(message, data)

    # menu_legal_address
    async def menu_legal_address(self, call: types.CallbackQuery, state: FSMContext):
        await self.legalAddress_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataLegalAddress,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_legal_address
    async def menu_get_legal_address(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["legalAddress"] = message.text
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
            data.get("individual")["pinfl"] = message.text
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
            data.get("individual")["paymentAccount"] = message.text
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
            data.get("individual")["bank"] = message.text
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
            data.get("individual")["mfo"] = message.text
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
            phone = phonenumbers.parse("+" + message.text)
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            data.get("individual")["phone"] = phone
            await self._change_data(message, data)

    # menu_end
    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuBlogger:menuBlogger_level1")
        async with state.proxy() as data:
            Lang, reply = await self._prepare_end(data)
            await self._end(call, data, Lang, reply)
            await self._add_entity(data)
            data.pop("entity")
            data.pop("individual")
            data.pop("selfEmployedCard")
            data.pop("selfEmployedAccount")

    @staticmethod
    async def _prepare_end(data):
        Lang: Model = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        return Lang, reply

    @staticmethod
    async def _end(call, data, Lang, reply):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        await bot.send_message(chat_id=call.from_user.id, text=Lang.start.greeting,
                               reply_markup=await reply.menu_blogger())

    @staticmethod
    async def _add_entity(data):
        json = await func.add_entity(data=data.get("individual"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_personal_data, text="individual",                                  state="PersonalDataIndividualBlogger:personalData_level1")
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=self.personalData_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.personalData_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back",                                          state=[self.title_level1,
                                                                                                                               self.legalAddress_level1,
                                                                                                                               self.pinfl_level1,
                                                                                                                               self.paymentAccount_level1,
                                                                                                                               self.bank_level1,
                                                                                                                               self.mfo_level1,
                                                                                                                               self.phone_level1])

        dp.register_callback_query_handler(self.menu_title, text="title",                                               state=self.personalData_level2)
        dp.register_callback_query_handler(self.menu_legal_address, text="legalAddress",                                state=self.personalData_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                               state=self.personalData_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.personalData_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.personalData_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.personalData_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.personalData_level2)

        dp.register_message_handler(self.menu_get_title, IsTitle(), content_types="text",                               state=self.title_level1)
        dp.register_message_handler(self.menu_get_legal_address, IsLegalAddress(), content_types="text",                state=self.legalAddress_level1)
        dp.register_message_handler(self.menu_get_pinfl, IsPinfl(), content_types="text",                               state=self.pinfl_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.personalData_level1)

