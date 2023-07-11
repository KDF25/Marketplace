from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, \
    MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from filters.personal_data import IsFio, IsNumber, IsDate, IsPinfl, IsPaymentAccount, IsBank, IsMfo, IsPhone, \
    IsCardNumber, IsCardDate
from filters.wallet import IsWithdraw
from handlers.group.send_withdraw import SendWithdraw
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from text.common.formSelfEmployedCardData import FormSelfEmployedCardData
from text.common.formWallet import FormWallet
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class WithdrawSelfEmployedCardBlogger(StatesGroup):

    withdraw_level1 = State()
    withdraw_level2 = State()
    withdraw_level3 = State()
    withdraw_level4 = State()
    withdraw_level5 = State()

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

    async def menu_personal_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.withdraw_level1.set()
        async with state.proxy() as data:
            await self._callback_data(data=data)
            Lang, inline, form = await self._prepare(data=data)
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_personal_data(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_first_data())

    @staticmethod
    async def _callback_data(data):
        if data.get("selfEmployedCard") is None:
            data["selfEmployedCard"] = {}
        data.get("selfEmployedCard")["cash"] = data.get("cash")

    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._change_data(message, data)

    async def _change_data(self, message, data):
        await self.withdraw_level2.set()
        Lang, inline, form = await self._prepare(data)
        await self._change(message, inline, form, data)

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormSelfEmployedCardData(data=data.get("selfEmployedCard"), language=data.get('lang'), email=data.get("email"))
        return Lang, inline, form

    @staticmethod
    async def _change(message: Union[types.Message, types.CallbackQuery], inline, form, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_self_employed_card())
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
            data.get("selfEmployedCard")["fio"] = message.text
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
            data.get("selfEmployedCard")["number"] = message.text
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
            data.get("selfEmployedCard")["date"] = message.text
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
            data.get("selfEmployedCard")["pinfl"] = message.text
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
            data.get("selfEmployedCard")["paymentAccount"] = message.text
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
            data.get("selfEmployedCard")["bank"] = message.text
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
            data.get("selfEmployedCard")["mfo"] = message.text
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
            data.get("selfEmployedCard")["phone"] = message.text
            await self._change_data(message, data)

    # menu_card_number
    async def menu_card_number(self, call: types.CallbackQuery, state: FSMContext):
        await self.cardNumber_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataCardNumber,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_card_number
    async def menu_get_card_number(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedCard")["cardNumber"] = message.text
            await self._change_data(message, data)

    # menu_card_date
    async def menu_card_date(self, call: types.CallbackQuery, state: FSMContext):
        await self.cardDate_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataCardDate,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu_get_card_number
    async def menu_get_card_date(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("selfEmployedCard")["cardDate"] = message.text
            await self._change_data(message, data)


    async def menu_cash(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_cash(call=call, data=data)

    async def _callback_cash(self, call, data):
        if call.data == "confirm":
            await self._check_data(data=data, call=call)
        elif call.data == "back":
            Lang, inline, form_wallet = await self._prepare_wallet(data=data)
            await self._cash( call=call, form_wallet=form_wallet, inline=inline)

    @staticmethod
    async def _prepare_wallet(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormWallet(data=data, language=data.get('lang'))
        return Lang, inline, form

    async def _check_data(self, data, call):
        Lang, inline, form_wallet = await self._prepare_wallet(data=data)
        if len(data.get("selfEmployedCard")) != 11:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
        else:
            await self._cash(call=call, form_wallet=form_wallet, inline=inline)
            await self._add_self_employed(data=data)

    @staticmethod
    async def _add_self_employed(data):
        json = await func.add_self_employed_card(data=data.get("selfEmployedCard"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    async def _cash(self, call, form_wallet, inline):
        await self.withdraw_level2.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form_wallet.menu_withdraw(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def _cash_back(self, call, form_wallet, inline, data):
        await self.withdraw_level2.set()
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get("message_id"))
        message = await bot.send_message(chat_id=call.from_user.id,
                                         text=await form_wallet.menu_withdraw(),
                                         reply_markup=await inline.menu_back())
        data["message_id"] = message.message_id

    async def menu_withdraw(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await self._check_withdraw(message=message, data=data)
            print(111, data)

    async def _check_withdraw(self, message, data):
        Lang, inline, form = await self._prepare(data=data)
        if int(message.text)  > data.get("wallet"):
            await self._not_enough_money(message=message, data=data, inline=inline, Lang=Lang)
        else:
            data.get("selfEmployedCard")["cash"] = int(message.text)
            await self._withdraw(message=message, data=data, inline=inline, form=form)

    @staticmethod
    async def _not_enough_money(message, data, inline, Lang):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get("message_id"))
        message = await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.notEnoughMoneyOnWallet,
                                         reply_markup=await inline.menu_back())
        data["message_id"] = message.message_id

    async def _withdraw(self, message, data, inline, form):
        await self.withdraw_level3.set()
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get("message_id"))
        message = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_withdraw(),
                                         reply_markup=await inline.menu_confirm())
        data["message_id"] = message.message_id

    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuBlogger:menuBlogger_level1")
        async with state.proxy() as data:
            await self._self_employed(call=call,data=data)
            await self._send_group(data=data)
            data.pop("entity")
            data.pop("individual")
            data.pop("selfEmployedCard")
            data.pop("selfEmployedCard")

    async def _self_employed(self, call, data):
        Lang, reply, form_wallet = await self._prepare_end(data=data)
        await self._end(call=call, data=data, form_wallet=form_wallet, reply=reply)

    @staticmethod
    async def _end(call, data, form_wallet, reply):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get("message_id"))
        await bot.send_message(chat_id=call.from_user.id, text=await form_wallet.menu_end(type_legal="selfEmployedCard"),
                               reply_markup=await reply.menu_blogger())

    @staticmethod
    async def _prepare_end(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        form_wallet = FormWallet(cash=data.get('selfEmployedCard').get("cash"), language=data.get('lang'))
        return Lang, reply, form_wallet

    @staticmethod
    async def _send_group(data):
        send_group = SendWithdraw(data=data, type_legal="selfEmployedCard")
        await send_group.start()

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_personal_data, text="selfEmployedCard",                            state="WalletBlogger:withdraw_level1")
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=self.withdraw_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.withdraw_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back",                                          state=[self.fio_level1,
                                                                                                                               self.number_level1,
                                                                                                                               self.date_level1,
                                                                                                                               self.pinfl_level1,
                                                                                                                               self.paymentAccount_level1,
                                                                                                                               self.bank_level1,
                                                                                                                               self.mfo_level1,
                                                                                                                               self.phone_level1,
                                                                                                                               self.cardNumber_level1,
                                                                                                                               self.cardDate_level1
                                                                                                                               ])

        dp.register_callback_query_handler(self.menu_fio, text="fio",                                                   state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_number, text="number",                                             state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_date, text="date",                                                 state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_pinfl, text="pinfl",                                               state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_card_number, text="cardNumber",                                    state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_card_date, text="cardDate",                                        state=self.withdraw_level2)

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

        dp.register_callback_query_handler(self.menu_cash, text="confirm",                                              state=self.withdraw_level1)
        dp.register_callback_query_handler(self.menu_cash, text="back",                                                 state=self.withdraw_level3)

        dp.register_message_handler(self.menu_withdraw, IsWithdraw(), content_types="text",                             state=self.withdraw_level2)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.withdraw_level3)
