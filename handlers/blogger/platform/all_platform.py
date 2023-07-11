from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from config import bot
from keyboards.inline.blogger.platform import InlinePlatformBlogger
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from model.form_order import ChannelListModel, OtherModel
from model.platform import GetPlatform
from text.blogger.formPlatform import FormPlatform
from text.language.main import Text_main
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class PlatformBlogger(StatesGroup):

    platform_level1 = State()
    platform_level2 = State()
    price_level1 = State()

    async def menu_all_platform(self,   message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.platform_level1.set()
        async with state.proxy() as data:
            await self._data_all_platform(data=data)
            await self._get_platforms(data=data)
            Lang, reply, inline, form = await self._prepare(data=data)
            if isinstance(message, types.Message):
                await self._all_platform(message=message, Lang=Lang, reply=reply, inline=inline, form=form, data=data)
            elif isinstance(message, types.CallbackQuery):
                await self._all_platform_back(message=message, inline=inline, form=form)

    @staticmethod
    async def _data_all_platform(data):
        if data.get('siteRequest') is None:
            data['siteRequest'] = OtherModel(offset=0, limit=Txt.limit.blogger.allPlatform)

    async def menu_all_platform_turn(self,   call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_all_platform(data=data, call=call)
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._all_platform_back(message=call, inline=inline, form=form)

    async def _callback_all_platform(self, call, data):
        limit = data.get('siteRequest').get('limit')
        pages = data.get('siteRequest').get('pages')
        page = data.get('siteRequest').get('page')
        if call.data == "prev" and page > 1:
            data.get('siteRequest')['offset'] -= limit
            data.get('siteRequest')['page'] -= 1
            await self._get_platforms(data=data)
        elif call.data == "next" and page < pages:
            data.get('siteRequest')['offset'] += limit
            data.get('siteRequest')['page'] += 1
            await self._get_platforms(data=data)

    @staticmethod
    async def _get_platforms(data):
        params = GetPlatform(language=data.get("lang"), offset=data.get('siteRequest').get("offset"),
                             limit=data.get('siteRequest').get("limit"))
        json = await fastapi.get_areas(token=data.get("token"), params=params)
        data["all_platform"] = await func.get_all_platform(json=json["channels"])
        page = data.get('siteRequest').get('offset') // data.get('siteRequest').get('limit') + 1
        page = page if json['pages'] != 0 else 0
        data["siteRequest"].update(ChannelListModel(count=json['count'], pages=json['pages'], page=page))

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        inline = InlinePlatformBlogger(language=data.get('lang'), platform=data.get("all_platform"),
                                       siteRequest=data.get("siteRequest"))
        form = FormPlatform(data=data.get("all_platform"), language=data.get('lang'))
        return Lang, reply, inline, form

    @staticmethod
    async def _all_platform(message, Lang, reply, inline, form, data):
        await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.platform,
                               reply_markup=await reply.main_menu())
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_all_platform(),
                                          reply_markup=await inline.menu_all_platform(), disable_web_page_preview=True)
        data['message_id'] = message1.message_id

    @staticmethod
    async def _all_platform_back(message, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                        text=await form.menu_all_platform(), reply_markup=await inline.menu_all_platform(),
                                        disable_web_page_preview=True)

    async def menu_preview(self, call: types.CallbackQuery, state: FSMContext):
        await self.platform_level1.set()
        async with state.proxy() as data:
            await self._callback_preview(data=data, call=call)
            inline, form = await self._prepare_preview(data=data)
            await self._preview(call=call, inline=inline, form=form)

    async def _callback_preview(self, data, call):
        dta = call.data.split("_")
        if dta[0] == "platform":
            await self._get_platform(data=data, call=call)

    @staticmethod
    async def _prepare_preview(data):
        inline = InlinePlatformBlogger(language=data.get('lang'))
        form = FormPlatform(data=data.get("current_platform"), language=data.get("lang"))
        return inline, form

    @staticmethod
    async def _get_platform(data, call):
        params = GetPlatform(language=data.get("lang"), area_id=int(call.data.split("_")[1]))
        json = await fastapi.get_area(token=data.get("token"), params=params)
        data["current_platform"] = await func.get_platform(json=json)

    @staticmethod
    async def _preview(call, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_change(),
                                        message_id=call.message.message_id, disable_web_page_preview=True,
                                        reply_markup=await inline.menu_preview())

    def register_handlers_platform_blogger(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_all_platform, text=Txt.menu.platform,                                     state="MenuBlogger:menuBlogger_level1")
        dp.register_callback_query_handler(self.menu_all_platform, text="back",                                         state=["AddPlatformBlogger:addPlatform_level1",
                                                                                                                               self.platform_level1])
        dp.register_callback_query_handler(self.menu_all_platform_turn, text=["prev", "next"],                          state=self.platform_level1)

        dp.register_callback_query_handler(self.menu_preview, lambda x: x.data.startswith("platform"),                  state=self.platform_level1)
        dp.register_callback_query_handler(self.menu_preview, text="back",                                              state=["ChangePlatformBlogger:changePlatform_level1",
                                                                                                                               "DeletePlatformBlogger:deletePlatform_level1",
                                                                                                                               "CalendarBlogger:calendar_level1"])

