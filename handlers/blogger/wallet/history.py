from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from config import bot
from keyboards.inline.common.wallet import InlineWalletUser
from looping import fastapi
from text.common.formWallet import FormWallet
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class HistoryWalletBlogger(StatesGroup):

    async def menu_history(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["history"] = {"offset": 0, "limit": 5}
            await self._get_events(call, data)

    async def _get_events(self, call, data):
        params = data.get("history")
        status, events = await fastapi.get_history_wallet(params=params, token=data.get("token"))
        print(events)
        if status == 200:
            if len(events) == 0:
                Lang: Model = Txt.language[data.get('lang')]
                await call.answer(text=Lang.alert.common.zeroCount, show_alert=True)
            else:
                await call.answer()
                await self._send_events(events=events, call=call, data=data)
        else:
            await call.answer()

    async def _send_events(self, events, call, data):
        for index, event in enumerate(events):
            if index+1 != data.get("history").get("limit"):
                await self._send_event(call=call, event=event, data=data)
            else:
                await self._send_event_last(call=call, event=event, data=data)

    @staticmethod
    async def _send_event(call, event, data):
        form = FormWallet(data=event, language=data.get("lang"))
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_history(), disable_web_page_preview=True)

    @staticmethod
    async def _send_event_last(call, event, data):
        form = FormWallet(data=event, language=data.get("lang"))
        inline = InlineWalletUser(language=data.get("lang"))
        await bot.send_message(chat_id=call.from_user.id, text=await form.menu_history(),
                               reply_markup=await inline.menu_history(), disable_web_page_preview=True)

    async def menu_more_history(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data.get("history")["offset"] += data.get("history").get("limit")
            await self._get_events(call, data)

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_history, text="history",                                           state=["WalletBlogger:walletBlogger_level1", "*"])
        dp.register_callback_query_handler(self.menu_more_history, text="moreHistory",                                  state=["WalletBlogger:walletBlogger_level1", "*"])

