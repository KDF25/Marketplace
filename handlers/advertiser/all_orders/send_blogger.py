from aiogram.utils.exceptions import BotBlocked

from config import bot
from keyboards.inline.blogger.newPost import InlinePostBlogger
from looping import pg, fastapi
from text.blogger.formNewOrder import FormNewOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class SendMessageBlogger:

    def __init__(self, text, data: dict, token: dict):
        self.__blogger_area_id = None
        self.__user_id = None
        self.__data = data
        self.__text = text
        self.__token = token

    async def send_blogger(self):
        for client in self.__data.get("owners"):
            users = await pg.select_users(client_id=client.get("owner"))
            status, json = await self._get_post(blogger_area_id=client.get("blogger_area_id"))
            for user_id in users:
                await self._post(user_id[0], json, client.get("blogger_area_id"))

    async def _post(self, user_id, json, blogger_area_id):
        try:
            await self._send_post(user_id, json, blogger_area_id)
        except BotBlocked:
            await pg.block_status(user_id=user_id, status=False)

    async def _get_post(self, blogger_area_id):
        status, json = await fastapi.project_blogger(blogger_area_id=blogger_area_id, token=self.__token)
        return status, json

    async def _send_post(self, user_id, json, blogger_area_id):
        lang = await pg.select_language(user_id=user_id)
        form = FormNewOrder(data=json, language=lang)
        inline = InlinePostBlogger(language=lang, order_id=self.__data.get("order_id"), blogger_area_id=blogger_area_id)
        text = await form.menu_send_advertiser(message_text=self.__text)
        await bot.send_message(chat_id=user_id, text=text, parse_mode="html",
                               reply_markup=await inline.menu_send_blogger(), disable_web_page_preview=True)


