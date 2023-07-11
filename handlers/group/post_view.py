from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import WrongFileIdentifier

from config import bot, moderation_chat_id
from aiogram.types.input_file import InputFile
from keyboards.inline.common.post_view import InlinePostView
from looping import fastapi
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FavorPostView(StatesGroup):

    accept_level1 = State()
    reject_level1 = State()
    cancel_level1 = State()
    sendAdvertiser_level1 = State()

    # menu check post
    async def menu_check_post(self, call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as data:
            await self._send_post(call, data)

    @staticmethod
    async def _post_accept(call):
        order_id = int(call.data.split("_")[1])
        params = {"order_id": order_id}
        status, json = await fastapi.get_post_moderation(params=params)
        return status, json

    @staticmethod
    async def _prepare_post(data, json):
        text = json.get("post_text")
        inline = InlinePostView(language="rus", url_buttons=json.get("buttons"))
        return text, inline

    async def _send_post(self, call, data):
        status, json = await self._post_accept(call)
        text, inline = await self._prepare_post(data, json)
        if json.get("photo") is not None:
            await self._post_photo(text, inline, json)
        elif json.get("video") is not None:
            await self._post_video(text, inline, json)
        else:
            await self._post_text(text, inline)
        if len(json.get('files')) != 0:
            await self._post_document(json)

    @staticmethod
    async def _post_text(text, inline):
        await bot.send_message(chat_id=moderation_chat_id, text=text, reply_markup=await inline.menu_post(),
                               parse_mode="html", disable_web_page_preview=True)

    @staticmethod
    async def _post_photo(text, inline, json):
        await bot.send_photo(chat_id=moderation_chat_id, caption=text, photo=json.get("photo"), parse_mode="html",
                             reply_markup=await inline.menu_post())

    @staticmethod
    async def _post_video(text, inline, json):
        video = json.get("video")
        try:
            await bot.send_video(chat_id=moderation_chat_id, caption=text, video=video, parse_mode="html",
                                 reply_markup=await inline.menu_post())
        except WrongFileIdentifier:
            video = InputFile.from_url(video)
            await bot.send_video(chat_id=moderation_chat_id, caption=text, video=video, parse_mode="html",
                                 reply_markup=await inline.menu_post())

    @staticmethod
    async def _post_document(json):
        document = json.get("files")[0]
        try:
            await bot.send_document(chat_id=moderation_chat_id, document=document)
        except WrongFileIdentifier:
            document = InputFile.from_url(document)
            await bot.send_document(chat_id=moderation_chat_id, document=document)

    def register_handlers_post(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_check_post, lambda x: x.data.startswith("FavorCheckPost"),         state="*")






