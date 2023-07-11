from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, BotBlocked

from config import bot
from keyboards.inline.blogger.platform import InlinePlatformBlogger
from looping import fastapi, pg
from text.blogger.formNewOrder import FormNewOrder
from text.blogger.formPlatform import FormPlatform
from text.language.main import Text_main

Txt = Text_main()


class DeletePlatformBlogger(StatesGroup):
    deletePlatform_level1 = State()
    deletePlatform_level2 = State()

    async def menu_delete(self, call: types.CallbackQuery, state: FSMContext):
        await self.deletePlatform_level1.set()
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            inline = InlinePlatformBlogger(language=data.get('lang'))
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.delete,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_delete())

    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        await self.deletePlatform_level2.set()
        async with state.proxy() as data:
            form = FormPlatform(data=data.get("current_platform"), language=data.get("lang"))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_delete_end(),
                                            message_id=call.message.message_id, disable_web_page_preview=True)
                json = await fastapi.delete_area(token=data.get("token"), area_id=data.get("current_platform").get("id"))
                await self._send_users(main_json=json)
                data.pop("current_platform")

    async def _send_users(self, main_json):
        for json in main_json.get("blogger_orders"):
            json.update({"area_url": main_json["url"]})
            json.update({"area_name": main_json["name"]})
            await self._user_reject(json=json)

    @staticmethod
    async def _user_reject(json):
        users = await pg.select_users(client_id=json.get("advertiser_id"))
        for user_id in users:
            try:
                lang_user = await pg.select_language(user_id=user_id[0])
                form_user = FormNewOrder(language=lang_user, data=json)
                await bot.send_message(chat_id=user_id[0], text=await form_user.menu_reject(), disable_web_page_preview=True)
            except BotBlocked:
                await pg.block_status(user_id=user_id[0], status=False)

    def register_handlers_delete_platform_blogger(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_delete, text="delete",                                             state="PlatformBlogger:platform_level1")
        dp.register_callback_query_handler(self.menu_end, text="deleteAnyway",                                          state=self.deletePlatform_level1)

