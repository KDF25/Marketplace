from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted, MessageToEditNotFound

from config import bot
from keyboards.inline.common.wallet import InlineWalletUser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from model.wallet import WalletModel
from text.common.formWallet import FormWallet
from text.language.main import Text_main
from filters.personal_data import IsNumber, IsMinPayment
from text.fuction.function import TextFunc


Txt = Text_main()
func = TextFunc()


class PaymentCommonAdvertiser(StatesGroup):
    paymentCommon_level1 = State()
    paymentCommon_level2 = State()
    paymentCommon_level3 = State()
    paymentCommon_level4 = State()
    paymentCommon_level5 = State()
    paymentCommon_level6 = State()

    @staticmethod
    async def _prepare(data):
        form = FormWallet(data=data, language=data.get("lang"))
        inline = InlineWalletUser(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        return Lang, form, inline

    # menu cash
    async def menu_cash(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlineWalletUser(language=data.get('lang'))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=Lang.wallet.putOn, reply_markup=await inline.menu_back())

    # menu employment
    async def menu_employment(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.paymentCommon_level2.set()
        async with state.proxy() as data:
            Lang, form, inline = await self._prepare_employment(data=data)
            if isinstance(message, types.Message):
                data["cash"] = int(message.text)
                await self._employment(message=message, form=form, inline=inline, data=data)
            elif isinstance(message, types.CallbackQuery):
                await self._employment_back(message=message, form=form, inline=inline)

    @staticmethod
    async def _employment(message: types.Message, form, inline, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_payment_start(),
                                          reply_markup=await inline.menu_employment())
        data['message_id'] = message1.message_id

    @staticmethod
    async def _prepare_employment(data):
        Lang = Txt.language[data.get('lang')]
        form = FormWallet(data=data, language=data.get("lang"))
        inline = InlineWalletUser(language=data.get('lang'))
        return Lang, form, inline

    @staticmethod
    async def _employment_back(message: types.CallbackQuery, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                        text=await form.menu_payment_start(), reply_markup=await inline.menu_employment())

    # menu self employment
    async def menu_self_employed(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level3.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlineWalletUser(language=data.get('lang'))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=Lang.wallet.choose, reply_markup=await inline.menu_self_employed())

    # menu payme
    async def menu_payme(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level4.set()
        async with state.proxy() as data:
            data["method"] = "Payme"
            Lang, form, inline = await self._prepare(data=data)
            await self._payment(call=call, form=form, inline=inline)

    # menu click
    async def menu_click(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level4.set()
        async with state.proxy() as data:
            data["method"] = "Click"
            Lang, form, inline = await self._prepare(data=data)
            await self._payment(call=call, form=form, inline=inline)

    # menu success payment click or payme
    async def menu_success(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuAdvertiser:menuAdvertiser_level1")
        async with state.proxy() as data:
            reply = ReplyUser(language=data.get('lang'))
            Lang, form, inline = await self._prepare(data=data)
            await self._success_payment(data=data)
            await self._success(call=call, form=form)

    @staticmethod
    async def _payment(call: types.CallbackQuery, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_payment(), reply_markup=await inline.menu_payment())

    @staticmethod
    async def _success(call: types.CallbackQuery, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_success())


    async def _success_payment(self, data):
        if data.get("method") == "Payme":
            await self._payme(data=data)
        elif data.get("method") == "Click":
            await self._click(data=data)

    @staticmethod
    async def _payme(data):
        json = WalletModel(amount=data.get("cash"))
        await fastapi.payment_payme(json=json, token=data.get("token"))

    @staticmethod
    async def _click(data):
        json = WalletModel(amount=data.get("cash"))
        await fastapi.payment_click(json=json, token=data.get("token"))

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_cash, text="balance",                                              state="WalletAdvertiser:walletAdvertiser_level1")
        dp.register_callback_query_handler(self.menu_cash, text="back",                                                 state=self.paymentCommon_level2)

        dp.register_message_handler(self.menu_employment, IsMinPayment(), content_types="text",                             state=self.paymentCommon_level1)
        dp.register_callback_query_handler(self.menu_employment, text="back",                                           state=[self.paymentCommon_level3,
                                                                                                                               "PaymentEntityAdvertiser:payment_level1",
                                                                                                                               "PaymentIndividualAdvertiser:payment_level1"
                                                                                                                               ])

        dp.register_callback_query_handler(self.menu_self_employed, text="selfEmployed",                                state=self.paymentCommon_level2)
        dp.register_callback_query_handler(self.menu_self_employed, text="back",                                        state=[self.paymentCommon_level4,
                                                                                                                               "PaymentSelfEmployedAccountAdvertiser:payment_level1"])

        dp.register_callback_query_handler(self.menu_payme, text="payme",                                               state=self.paymentCommon_level3)

        dp.register_callback_query_handler(self.menu_click, text="click",                                               state=self.paymentCommon_level3)

        dp.register_callback_query_handler(self.menu_success, text="payment",                                           state=self.paymentCommon_level4)
