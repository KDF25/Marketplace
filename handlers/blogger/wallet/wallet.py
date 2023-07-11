from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from config import bot
from keyboards.inline.common.wallet import InlineWalletUser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from text.common.formWallet import FormWallet
from text.language.main import Text_main
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class WalletBlogger(StatesGroup):

    walletBlogger_level1 = State()
    withdraw_level1 = State()

    # menu wallet
    async def menu_wallet(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.walletBlogger_level1.set()
        async with state.proxy() as data:
            await self._exist_personal_data(data=data)
            await self.get_balance(data=data)
            form, inline, Lang, reply = await self._prepare(data=data)
            if isinstance(message, types.Message):
                await self._wallet(message=message, form=form, inline=inline, Lang=Lang, reply=reply, data=data)
            elif isinstance(message, types.CallbackQuery):
                await self._wallet_back(message=message, form=form, inline=inline)

    @staticmethod
    async def get_balance(data):
        json = await fastapi.get_balance(token=data.get("token"))
        data["wallet"] = json.get("balance", 0)

    @staticmethod
    async def _exist(token):
        json = await fastapi.get_active_legal(token=token)
        return json

    async def _exist_personal_data(self, data):
        json = await self._exist(token=data.get("token"))
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
        form = FormWallet(data=data, language=data.get("lang"))
        inline = InlineWalletUser(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        return form, inline, Lang, reply

    @staticmethod
    async def _wallet(message, form, inline, Lang, reply, data):
        await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.wallet,
                               reply_markup=await reply.main_menu())
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_wallet(),
                                          reply_markup=await inline.menu_wallet())
        data['message_id'] = message1.message_id

    @staticmethod
    async def _wallet_back(message, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                   text=await form.menu_wallet(), reply_markup=await inline.menu_wallet())

    # menu withdraw_start
    async def menu_withdraw_start(self, call: types.CallbackQuery, state: FSMContext):
        await self.withdraw_level1.set()
        async with state.proxy() as data:
            form, inline, Lang, reply = await self._prepare(data=data)
            await self._withdraw_start(call=call, form=form, inline=inline)

    @staticmethod
    async def _withdraw_start(call: types.CallbackQuery, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_withdraw_start(), reply_markup=await inline.menu_employment2())

    def register_handlers(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_wallet, text=Txt.menu.wallet,                                              state="MenuBlogger:menuBlogger_level1")
        dp.register_callback_query_handler(self.menu_wallet, text="back",                                               state=["PaymentCommonBlogger:paymentCommon_level1",
                                                                                                                               self.withdraw_level1])
        dp.register_callback_query_handler(self.menu_withdraw_start, text="withdraw",                                   state=self.walletBlogger_level1)
        dp.register_callback_query_handler(self.menu_withdraw_start, text="back",                                       state=["WithdrawEntityBlogger:withdraw_level1",
                                                                                                                               "WithdrawIndividualBlogger:withdraw_level1",
                                                                                                                               "WithdrawSelfEmployedAccountBlogger:withdraw_level1",
                                                                                                                               "WithdrawSelfEmployedCardBlogger:withdraw_level1"])

