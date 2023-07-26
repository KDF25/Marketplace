from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import *

from config import bot
from handlers.advertiser.form_order.send_blogger import SendBlogger
from keyboards.inline.common.wallet import InlineWalletUser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from model.wallet import WalletModel
from text.common.formWallet import FormWallet
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormOrderPaymentCommon(StatesGroup):
    paymentCommon_level1 = State()
    paymentCommon_level2 = State()
    paymentCommon_level3 = State()
    paymentCommon_level4 = State()
    paymentCommon_level5 = State()
    paymentCommon_level6 = State()

    @staticmethod
    async def _prepare(data):
        cash = abs(int(data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet")))
        form = FormWallet(data=data, language=data.get("lang"),  cash=cash)
        inline = InlineWalletUser(language=data.get('lang'))
        Lang: Model = Txt.language[data.get('lang')]
        return form, inline, Lang

    # menu self employed
    async def menu_self_employed(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level1.set()
        async with state.proxy() as data:
            form = FormWallet(language=data.get("lang"),
                              cash=int(data .get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet")))
            inline = InlineWalletUser(language=data.get('lang'))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form.menu_payment_start2(), reply_markup=await inline.menu_self_employed())

    # menu payme
    async def menu_payme(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level2.set()
        async with state.proxy() as data:
            data["method"] = "Payme"
            form, inline, Lang = await self._prepare(data)
            await self._payment(call, form, inline)

    @staticmethod
    async def _payment(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_payment2(), reply_markup=await inline.menu_payment())

    # menu click
    async def menu_click(self, call: types.CallbackQuery, state: FSMContext):
        await self.paymentCommon_level2.set()
        async with state.proxy() as data:
            data["method"] = "Click"
            form, inline, Lang = await self._prepare(data)
            await self._payment(call, form, inline)

    # menu success
    async def menu_success(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuAdvertiser:menuAdvertiser_level1")
        async with state.proxy() as data:
            reply = ReplyUser(language=data.get('lang'))
            await self._success(call, data, reply)
            await self._success_payment(data)
            await self._send_blogger(data=data)
            data.pop("formOrder")

    @staticmethod
    async def _success(call, data, reply):
        Lang: Model = Txt.language[data.get("lang")]
        await call.answer(show_alert=True, text=Lang.alert.advertiser.startCampaign)
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        json = {"cash": int(data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet"))}
        form = FormWallet(language=data.get("lang"), data=json)
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_success())
        await bot.send_message(chat_id=call.from_user.id,  text=await form.menu_success_campaign(int(data.get("formOrder").get("basket").get("total_cost"))),
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    async def _success_payment(self, data):
        if data.get("method") == "Payme":
            await self._payme(data)
        elif data.get("method") == "Click":
            await self._click(data)

    @staticmethod
    async def _payme(data):
        amount = int(data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet"))
        json = WalletModel(amount=amount)
        await fastapi.payment_payme(json=json, token=data.get("token"))

    @staticmethod
    async def _click(data):
        amount = int(data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet"))
        json = WalletModel(amount=amount)
        await fastapi.payment_click(json=json, token=data.get("token"))

    @staticmethod
    async def _send_blogger(data):
        send_blogger = SendBlogger(data=data)
        await send_blogger.send()

    def register_handlers_form_order_payment(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_self_employed, text="selfEmployed",                                state="FormOrderWallet:walletFormOrder_level2")
        dp.register_callback_query_handler(self.menu_self_employed, text="back",                                        state=[self.paymentCommon_level2,
                                                                                                                               "FormOrderPaymentSelfEmployedAccount:payment_level1"])

        dp.register_callback_query_handler(self.menu_payme, text="payme",                                               state=self.paymentCommon_level1)
        dp.register_callback_query_handler(self.menu_click, text="click",                                               state=self.paymentCommon_level1)

        dp.register_callback_query_handler(self.menu_success, text="payment",                                           state=self.paymentCommon_level2)
