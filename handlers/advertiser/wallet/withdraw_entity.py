from contextlib import suppress
from typing import Union

import phonenumbers
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, MessageIdentifierNotSpecified, \
    MessageCantBeDeleted, MessageToEditNotFound

from config import bot
from filters.personal_data import *
from filters.wallet import IsWithdraw
from handlers.group.send_withdraw import SendWithdraw
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from text.common.formEntityData import FormEntityData
from text.common.formWallet import FormWallet
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class WithdrawEntityAdvertiser(StatesGroup):
    withdraw_level1 = State()
    withdraw_level2 = State()
    withdraw_level3 = State()
    withdraw_level4 = State()
    withdraw_level5 = State()

    title_level1 = State()
    legalAddress_level1 = State()
    inn_level1 = State()
    paymentAccount_level1 = State()
    bank_level1 = State()
    mfo_level1 = State()
    phone_level1 = State()

    async def menu_personal_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.withdraw_level1.set()
        async with state.proxy() as data:
            await self._callback_data(data=data)
            Lang, inline, form = await self._prepare(data=data)
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_personal_data(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_first_data())
            print(data)

    @staticmethod
    async def _callback_data(data):
        if data.get('entity') is None:
            data["entity"] = {}
        data.get("entity")["cash"] = data.get("cash")

    async def menu_change_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.withdraw_level2.set()
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
        form = FormEntityData(data=data.get("entity"), language=data.get('lang'), email=data.get("email"))
        return Lang, inline, form

    @staticmethod
    async def _change(message: Union[types.Message, types.CallbackQuery], inline, form, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                          reply_markup=await inline.menu_change_entity())
        data['message_id'] = message1.message_id

    async def _change_data(self, message, data):
        await self.withdraw_level2.set()
        Lang, inline, form = await self._prepare(data)
        await self._change(message, inline, form, data)

    @staticmethod
    async def _change_edit(message: Union[types.Message, types.CallbackQuery], inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, text=await form.menu_change_data(),
                                        message_id=message.message.message_id, reply_markup=await inline.menu_change_entity())

    async def menu_title(self, call: types.CallbackQuery, state: FSMContext):
        await self.title_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataTitleEntity,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_title(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("entity")["title"] = message.text
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

    async def menu_get_legal_address(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("entity")["legalAddress"] = message.text
            await self._change_data(message, data)

    async def menu_inn(self, call: types.CallbackQuery, state: FSMContext):
        await self.inn_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            inline = InlinePersonalData(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.personalData.common.newDataInn,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_inn(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("entity")["inn"] = message.text
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

    async def menu_get_payment_account(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("entity")["paymentAccount"] = message.text
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

    async def menu_get_bank(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("entity")["bank"] = message.text
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

    async def menu_get_mfo(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            data.get("entity")["mfo"] = message.text
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

    async def menu_get_phone(self,  message: types.Message,  state: FSMContext):
        async with state.proxy() as data:
            phone = phonenumbers.parse("+" + message.text)
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            data.get("entity")["phone"] = phone
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
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form = FormWallet(data=data, language=data.get('lang'))
        return Lang, inline, form
        
    async def _check_data(self, data, call):
        Lang, inline, form_wallet = await self._prepare_wallet(data=data)
        if len(data.get("entity")) != 8:
            await call.answer(text=Lang.alert.common.allData, show_alert=True)
        else:
            await self._cash(call=call, form_wallet=form_wallet, inline=inline)
            await self._add_entity(data=data)

    async def _cash(self, call, form_wallet, inline):
        await self.withdraw_level2.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form_wallet.menu_withdraw(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    @staticmethod
    async def _add_entity(data):
        json = await func.add_entity(data=data.get("entity"))
        await fastapi.add_type_legal(json=json, token=data.get('token'))

    async def _cash_back(self, call, form_wallet, inline, data):
        await self.withdraw_level2.set()
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get("message_id"))
        message = await bot.send_message(chat_id=call.from_user.id, text=await form_wallet.menu_withdraw(),
                                         reply_markup=await inline.menu_back())
        data["message_id"] = message.message_id

    async def menu_withdraw(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await self._check_withdraw(message=message, data=data)

    async def _check_withdraw(self, message, data):
        Lang, inline, form = await self._prepare(data=data)
        if int(message.text)  > data.get("wallet"):
            await self._not_enough_money(message=message, data=data, inline=inline, Lang=Lang)
        else:
            data.get("entity")["cash"] = int(message.text)
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
        await state.set_state("MenuAdvertiser:menuAdvertiser_level1")
        async with state.proxy() as data:
            await self._entity(call=call, data=data)
            await self._send_group(data=data)
            data.pop("entity")
            data.pop("individual")
            data.pop("selfEmployedAccount")
            data.pop("selfEmployedCard")

    async def _entity(self, call, data):
        Lang, reply, form_wallet = await self._prepare_end(data=data)
        await self._end(call=call, data=data, form_wallet=form_wallet, reply=reply)

    @staticmethod
    async def _end(call, data, form_wallet, reply):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get("message_id"))
        await bot.send_message(chat_id=call.from_user.id, text=await form_wallet.menu_end(type_legal="entity"),
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _prepare_end(data):
        Lang: Model = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        form_wallet = FormWallet(cash=data.get('entity').get("cash"), language=data.get('lang'))
        return Lang, reply, form_wallet

    @staticmethod
    async def _send_group(data):
        send_group = SendWithdraw(data=data, type_legal="entity")
        await send_group.start()

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_personal_data, text="entity",                                      state="WalletAdvertiser:withdraw_level1")
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=self.withdraw_level2)

        dp.register_callback_query_handler(self.menu_change_data, text="changeData",                                    state=self.withdraw_level1)
        dp.register_callback_query_handler(self.menu_change_data, text="back",                                          state=[self.title_level1,
                                                                                                                               self.legalAddress_level1,
                                                                                                                               self.inn_level1,
                                                                                                                               self.paymentAccount_level1,
                                                                                                                               self.bank_level1,
                                                                                                                               self.mfo_level1,
                                                                                                                               self.phone_level1])

        dp.register_callback_query_handler(self.menu_title, text="title",                                               state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_legal_address, text="legalAddress",                                state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_inn, text="inn",                                                   state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_payment_account, text="paymentAccount",                            state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_bank, text="bank",                                                 state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_mfo, text="mfo",                                                   state=self.withdraw_level2)
        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.withdraw_level2)

        dp.register_message_handler(self.menu_get_title, IsTitle(), content_types="text",                               state=self.title_level1)
        dp.register_message_handler(self.menu_get_legal_address, IsLegalAddress(), content_types="text",                state=self.legalAddress_level1)
        dp.register_message_handler(self.menu_get_inn, IsInn(), content_types="text",                                   state=self.inn_level1)
        dp.register_message_handler(self.menu_get_payment_account, IsPaymentAccount(), content_types="text",            state=self.paymentAccount_level1)
        dp.register_message_handler(self.menu_get_bank, IsBank(), content_types="text",                                 state=self.bank_level1)
        dp.register_message_handler(self.menu_get_mfo, IsMfo(), content_types="text",                                   state=self.mfo_level1)
        dp.register_message_handler(self.menu_get_phone, IsPhone(), content_types="text",                               state=self.phone_level1)

        dp.register_callback_query_handler(self.menu_cash, text="confirm",                                              state=self.withdraw_level1)
        dp.register_callback_query_handler(self.menu_cash, text="back",                                                 state=self.withdraw_level3)

        dp.register_message_handler(self.menu_withdraw, IsWithdraw(), content_types="text",                                state=self.withdraw_level2)

        dp.register_callback_query_handler(self.menu_end, text="confirm",                                               state=self.withdraw_level3)

