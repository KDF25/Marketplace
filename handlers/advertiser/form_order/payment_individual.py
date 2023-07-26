from contextlib import suppress
from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import *

from filters.personal_data import *
from handlers.advertiser.form_order.send_blogger import SendBlogger
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.inline.common.wallet import InlineWalletUser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from model.wallet import WalletModel
from text.common.formIndividualData import FormIndividualData
from text.common.formWallet import FormWallet
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FormOrderPaymentIndividual(StatesGroup):
    payment_level1 = State()
    payment_level2 = State()

    title_level1 = State()
    legalAddress_level1 = State()
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

    @staticmethod
    async def _callback_data(data):
        if data.get("individual") is None:
            data["individual"] = {}
        data.get("individual")["cash"] = data.get("cash")

    async def _change_data(self, message, data):
        await self.payment_level2.set()
        Lang, inline, form = await self._prepare(data)
        await self._change(message, inline, form, data)

    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.payment_level2.set()
        async with state.proxy() as data:
            Lang, inline, form = await self._prepare(data=data)
            if isinstance(message, types.Message):
                await self._change(message=message, inline=inline, form=form, data=data)
            elif isinstance(message, types.CallbackQuery):
                if message.data == "changeData":
                    await self._change_edit(message=message, inline=inline, form=form)
                else:
                    await self._change(message=message, inline=inline, form=form, data=data)

    @staticmethod
    async def _prepare(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormIndividualData(data=data.get("individual"), language=data.get('lang'), email=data.get("email"))
        return Lang, inline, form

    @staticmethod
    async def _change(message: Union[types.Message, types.CallbackQuery], inline, form, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_individual())
        data['message_id'] = message1.message_id

    @staticmethod
    async def _change_edit(message: Union[types.Message, types.CallbackQuery], inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                        message_id=message.message.message_id,
                                        reply_markup=await inline.menu_change_individual())

    async def menu_title(self, call: types.CallbackQuery, state: FSMContext):
        await self.title_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataTitleIndividual,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_title(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["title"] = message.text
            await self._change_data(message, data)

    async def menu_legal_address(self, call: types.CallbackQuery, state: FSMContext):
        await self.legalAddress_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataLegalAddress,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_legal_address(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["legalAddress"] = message.text
            await self._change_data(message, data)

    async def menu_pinfl(self, call: types.CallbackQuery, state: FSMContext):
        await self.pinfl_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPinfl,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_pinfl(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["pinfl"] = message.text
            await self._change_data(message, data)

    async def menu_payment_account(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentAccount_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPaymentAccount,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_payment_account(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["paymentAccount"] = message.text
            await self._change_data(message, data)

    async def menu_bank(self, call: types.CallbackQuery, state: FSMContext):
        await self.bank_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataBank,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_bank(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["bank"] = message.text
            await self._change_data(message, data)

    async def menu_mfo(self, call: types.CallbackQuery, state: FSMContext):
        await self.mfo_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataMfo,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_mfo(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("individual")["mfo"] = message.text
            await self._change_data(message, data)

    async def menu_phone(self, call: types.CallbackQuery, state: FSMContext):
        await self.phone_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataPhone,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_phone(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            phone = phonenumbers.parse("+" + message.text)
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            data.get("individual")["phone"] = phone
            await self._change_data(message, data)

    # menu end
    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_data(call, data, state)

    async def _check_data(self, call, data, state):
        reply, inline, Lang = await self._prepare_wallet(data)
        if len(data.get("individual")) != 8:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
        else:
            await state.set_state("MenuAdvertiser:menuAdvertiser_level1")
            await self._add_individual(data)
            await self._payment_didox(data=data)
            await self._send_blogger(data=data)
            await self._success_payment(call, data, reply)
            data.pop("individual")
            data.pop("formOrder")

    @staticmethod
    async def _prepare_wallet(data):
        reply = ReplyUser(language=data.get('lang'))
        inline = InlineWalletUser(language=data.get('lang'))
        Lang: Model = Txt.language[data.get('lang')]
        return reply, inline, Lang

    @staticmethod
    async def _success_payment(call, data, reply):
        Lang: Model = Txt.language[data.get("lang")]
        await call.answer(show_alert=True, text=Lang.alert.advertiser.startCampaign)
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        form_wallet = FormWallet(language=data.get("lang"))
        await bot.send_message(chat_id=call.from_user.id, text=await form_wallet.menu_success_campaign(
            cash=data.get("formOrder").get("basket").get("total_cost")),
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _add_individual(data):
        json = await func.add_individual(data=data.get("individual"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    @staticmethod
    async def _payment_didox(data):
        json = WalletModel(type_legal="individual", amount=int(
            data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet")))
        await fastapi.payment_didox(json=json, token=data.get('token'))

    @staticmethod
    async def _send_blogger(data):
        send_blogger = SendBlogger(data=data)
        await send_blogger.send()

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_personal_data, text="individual",                                      state="FormOrderWallet:walletFormOrder_level2")
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=self.payment_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.payment_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back",                                          state=[self.title_level1,
                                                                                                                              self.legalAddress_level1,
                                                                                                                              self.pinfl_level1,
                                                                                                                              self.paymentAccount_level1,
                                                                                                                              self.bank_level1,
                                                                                                                              self.mfo_level1,
                                                                                                                              self.phone_level1])

        dp.register_callback_query_handler(self.menu_title, text="title",                                               state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_legal_address, text="legalAddress",                                state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                                   state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.payment_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.payment_level2)

        dp.register_message_handler(self.menu_get_title, IsTitle(), content_types="text",                               state=self.title_level1)
        dp.register_message_handler(self.menu_get_legal_address, IsLegalAddress(), content_types="text",                state=self.legalAddress_level1)
        dp.register_message_handler(self.menu_get_pinfl, IsPinfl(), content_types="text",                               state=self.pinfl_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.payment_level1)

