from contextlib import suppress
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from config import bot
from datetime_now import dt_now
from keyboards.inline.blogger.platform import InlinePlatformBlogger
from looping import fastapi
from model.calendar import CalendarModel
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class CalendarBlogger(StatesGroup):

    calendar_level1 = State()

    async def menu_calendar(self, call: types.CallbackQuery, state: FSMContext):
        await self.calendar_level1.set()
        async with state.proxy() as data:
            await self._callback_calendar(data=data)
            await self._get_info_month(data=data)
            Lang, inline = await self._prepare_calendar(data=data)
            await self._calendar(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _callback_calendar(data):
        now = dt_now.now()
        date = datetime.strftime(datetime(year=now.year, month=now.month, day=now.day), "%d.%m.%Y")
        data.get('current_platform')['current_date'] = date

    @staticmethod
    async def _get_info_month(data):
        area_id = data.get("current_platform").get('id')
        date = data.get('current_platform')['current_date']
        date = datetime.strptime(date, "%d.%m.%Y")
        params = CalendarModel(area_id=area_id, year=date.year, month=date.month)
        json = await fastapi.get_info_month(token=data.get('token'), params=params)
        data.get("current_platform")["calendar"] = [day.get("date") for day in json.get("days")]

    @staticmethod
    async def _prepare_calendar(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), token=data.get("token"),
                                       date=data.get('current_platform').get('current_date'),
                                       calendar_list=data.get("current_platform").get("calendar"))
        return Lang, inline

    @staticmethod
    async def _calendar(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.platform.blogger.calendar, reply_markup=await inline.menu_calendar())

    # menu calendar turn
    async def menu_calendar_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._calendar_turn(data=data, call=call)
            await self._get_info_month(data=data)
            Lang, inline = await self._prepare_calendar(data=data)
            await self._calendar(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _calendar_turn(data, call):
        date = await func.calendar(date=data.get('current_platform').get('current_date'), turn=call.data)
        data.get('current_platform')['current_date'] = date

    # menu set status
    async def menu_set_status(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            status = await self._set_status_on_day(data=data, call=call)
            await self._check_status(data=data, call=call, status=status)

    async def _check_status(self, data, call, status):
        Lang: Model = Txt.language[data.get('lang')]
        if status == "free":
            await call.answer(text=Lang.alert.blogger.free, show_alert=True)
            await self._success_set_status(data=data, call=call)
        elif status == "busy":
            await call.answer(text=Lang.alert.blogger.busy, show_alert=True)
            await self._success_set_status(data=data, call=call)
        elif status is None:
            await call.answer(text=Lang.alert.common.calendar, show_alert=True)

    async def _success_set_status(self, data, call):
        await self._get_info_month(data=data)
        Lang, inline = await self._prepare_calendar(data=data)
        await self._calendar(call=call, Lang=Lang, inline=inline)

    @staticmethod
    async def _set_status_on_day(data, call):
        area_id = data.get("current_platform").get('id')
        date = call.data.split("_")[1]
        date = datetime.strptime(date, "%d.%m.%Y")
        json = CalendarModel(area_id=area_id, year=date.year, month=date.month, day=date.day)
        json = await fastapi.set_status_on_day(token=data.get('token'), json=json)
        status = json.get("type_busy")
        return status

    def register_handlers_calendar(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_calendar, text="calendar",                                         state="PlatformBlogger:platform_level1")
        dp.register_callback_query_handler(self.menu_calendar_turn, text=['next', 'prev'],                              state=self.calendar_level1)
        dp.register_callback_query_handler(self.menu_set_status, lambda x: x.data.startswith("day"),                    state=self.calendar_level1)



