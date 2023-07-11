import datetime
from contextlib import suppress

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from config import bot
from filters.admin import IsAdmin
from keyboards.inline.admin.admin import InlineAdmin
from text.admin.formAdmin import FormAdmin
from text.language.main import Text_main

Txt = Text_main()
inline = InlineAdmin()
form = FormAdmin()
main_text = "Администраторская"


class Statistics(StatesGroup):
    statistics_level1 = State()
    statistics_level2 = State()
    statistics_level3 = State()

    async def menu_period(self, call: types.CallbackQuery, state: FSMContext):
        json = await self._period(call=call)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_statistics(json=json),
                                        message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, text=main_text, reply_markup=await inline.menu_admin())
            await state.set_state("MenuAdmin:menu_admin_level1")

    async def _period(self, call: types.CallbackQuery):
        from_date = datetime.date.today()
        until_date = datetime.date.today()
        if call.data == "day":
            until_date = from_date - datetime.timedelta(days=1)
        elif call.data == "week":
            until_date = from_date - datetime.timedelta(days=7)
        elif call.data == "month":
            until_date = from_date - datetime.timedelta(days=30)
        from_date = datetime.date.strftime(from_date, "%Y-%m-%d")
        until_date = datetime.date.strftime(until_date, "%Y-%m-%d")
        json = {"from_date": from_date, "until_date": until_date}
        return json

    def register_handlers_statistics(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_period, IsAdmin(), text=["day", 'week', "month"],                  state=self.statistics_level1)



