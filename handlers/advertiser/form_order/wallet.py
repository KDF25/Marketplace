from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, \
    MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from handlers.advertiser.form_order.send_blogger import SendBlogger

from keyboards.inline.common.wallet import InlineWalletUser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from text.common.formWallet import FormWallet
from text.language.main import Text_main
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FormOrderWallet(StatesGroup):

    walletFormOrder_level1 = State()
    walletFormOrder_level2 = State()

    # menu wallet
    async def menu_wallet(self, call: types.CallbackQuery, state: FSMContext):
        await self.walletFormOrder_level1.set()
        async with state.proxy() as data:
            await self._exist_personal_data(data=data)
            await self.get_balance(data=data)
            await self._check_balance(data=data, call=call, state=state)

    @staticmethod
    async def get_balance(data):
        json = await fastapi.get_balance(token=data.get("token"))
        data.get("formOrder")["wallet"] = json.get("balance", 0)

    @staticmethod
    async def _exist(data):
        json = await fastapi.get_active_legal(token=data.get("token"))
        return json

    async def _exist_personal_data(self, data):
        json = await self._exist(data=data)
        if json.get("type_legal") == "entity":
            data["entity"] = await func.get_entity(json=json)
        elif json.get("type_legal") == "individual":
            data["individual"] = await func.get_individual(json=json)
        elif json.get("type_legal") == "self_employed":
            data["selfEmployedAccount"] = await func.get_self_employed_account(json=json)
        elif json.get("type_legal") == "self_employed_transit":
            data["selfEmployedCard"] = await func.get_self_employed_card(json=json)

    @staticmethod
    async def _prepare(data):
        reply = ReplyUser(language=data.get('lang'))
        inline = InlineWalletUser(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        form = FormWallet(language=data.get("lang"),
                          cash=int(data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet")),
                          payment=int(data.get("formOrder").get("wallet") - data.get("formOrder").get("basket").get("total_cost")))
        return reply, inline, Lang, form

    async def _check_balance(self, data, call, state):
        reply, inline, Lang, form = await self._prepare(data=data)
        if data.get("formOrder").get("wallet") >= data.get("formOrder").get("basket").get("total_cost"):
            await state.set_state("MenuAdvertiser:menuAdvertiser_level1")
            await self._success_payment(call, data, reply)
            await self._send_blogger(data=data)
            data.pop("formOrder")
        elif data.get("formOrder").get("wallet") < data.get("formOrder").get("basket").get("total_cost"):
            await self._wallet(call, data, form, inline)

    @staticmethod
    async def _success_payment(call, data, reply):
        Lang = Txt.language[data.get("lang")]
        await call.answer(show_alert=True, text=Lang.alert.advertiser.startCampaign)
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        form = FormWallet(language=data.get("lang"))
        await bot.send_message(chat_id=call.from_user.id,
                               text=await form.menu_success_campaign(int(data.get("formOrder").get("basket").get("total_cost"))),
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _wallet(call, data,  form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            payment = int(data.get("formOrder").get("basket").get("total_cost") - data.get("formOrder").get("wallet"))
            form = FormWallet(language=data.get("lang"), payment=payment)
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_payment_campaign(),
                                        reply_markup=await inline.menu_payment_form_order())

    @staticmethod
    async def _send_blogger(data):
        send_blogger = SendBlogger(data=data)
        await send_blogger.send()

    # menu payment start
    async def menu_payment_start(self, call: types.CallbackQuery, state: FSMContext):
        await self.walletFormOrder_level2.set()
        async with state.proxy() as data:
            reply, inline, Lang, form = await self._prepare(data=data)
            await self._payment_start(call=call, form=form, inline=inline)

    @staticmethod
    async def _payment_start(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_payment_start2(), reply_markup=await inline.menu_employment())

    def register_handlers_form_order_wallet(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_wallet, text="order",                                              state="FormOrderAdvertiser:formOrderAdvertiser_level8")
        dp.register_callback_query_handler(self.menu_wallet, text="back",                                               state=["PaymentCommonBlogger:paymentCommon_level1",
                                                                                                                               self.walletFormOrder_level2])
        dp.register_callback_query_handler(self.menu_payment_start, text="balance",                                     state=self.walletFormOrder_level1)
        dp.register_callback_query_handler(self.menu_payment_start, text="back",                                        state=["FormOrderPaymentCommon:paymentCommon_level1",
                                                                                                                               "FormOrderPaymentEntity:payment_level1",
                                                                                                                               "FormOrderPaymentIndividual:payment_level1",
                                                                                                                               ])

