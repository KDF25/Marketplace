from aiogram.utils.exceptions import BotBlocked

from config import bot
from keyboards.inline.blogger.newPost import InlinePostBlogger
from looping import pg
from text.blogger.formNewOrder import FormNewOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class SendMessageAdvertiser:

    def __init__(self, text, data: dict, ):
        self.__data = data
        self.__user_id = None
        self.__text = text

    async def send_advertiser(self):
        users = await pg.select_users(client_id=self.__data.get("advertiser_id"))
        for user_id in users:
            self.__user_id = user_id[0]
            await self._post()

    async def _post(self):
        await self._prepare_post()
        try:
            await self._send_post()

        except BotBlocked:
            await pg.block_status(user_id=self.__user_id, status=False)

    async def _prepare_post(self):
        lang = await pg.select_language(user_id=self.__user_id)
        self.__form = FormNewOrder(data=self.__data, language=lang)
        self.__inline = InlinePostBlogger(language=lang, order_id=self.__data.get("order_id"),
                                          client_id=self.__data.get("blogger_id"))

    async def _send_post(self):
        text = await self.__form.menu_send_advertiser(message_text=self.__text)
        await bot.send_message(chat_id=self.__user_id, text=text,  reply_markup=await self.__inline.menu_send_advertiser(),
                               disable_web_page_preview=True)
