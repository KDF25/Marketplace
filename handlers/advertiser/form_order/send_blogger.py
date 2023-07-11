from aiogram.utils.exceptions import BotBlocked

from config import bot
from keyboards.inline.blogger.newPost import InlinePostBlogger
from looping import pg, fastapi
from model.form_order import PostModel
from text.advertiser.formOrder import FormOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

from typing import Any
from aiohttp import FormData, ClientSession, ClientResponse

Txt = Text_main()
func = TextFunc()

telegram_url = "https://api.telegram.org/file/bot5138329580:AAEedoAxPDvcW87Mr_h_ytSJf2HYdxfBQgM/{}"


class SendBlogger:

    def __init__(self, data: dict):
        self.__blogger_area_id = None
        self.__channel = None
        self.__data = data
        self.__client_id = None

    async def send(self):
        channels_response = await self._upload_post()
        print("channels_response2", channels_response)
        for basket_channel in self.__data.get('formOrder').get("basket").get("channels"):
            for channel in channels_response:
                if channel.get("area_id") == basket_channel.get("id"):
                    # self.__blogger_area_id = channel.get("id")
                    await self._send_blogger(basket_channel, channel.get("id"))
                    # break

    async def _send_blogger(self, channel,  blogger_area_id):
        users = await pg.select_users(client_id=channel["client_id"])
        for user_id in users:
            await self._post(channel, user_id[0],  blogger_area_id)

    async def _post(self, channel, user_id,  blogger_area_id):
        # try:
        await self._send_post(channel, user_id,  blogger_area_id)
        # except Exception:
        #     await pg.block_status(user_id=user_id, status=False)

    async def _send_post(self, channel, user_id,  blogger_area_id):
        lang = await pg.select_language(user_id=user_id)
        form = FormOrder(data=channel, language=lang)
        inline = InlinePostBlogger(language=lang, blogger_area_id= blogger_area_id,
                                   order_id=self.__data.get("formOrder").get("campaign").get("order_id"))
        text = await form.menu_send_blogger(comment=self.__data.get("formOrder").get("campaign").get("comment", "-"),
                                            name=self.__data.get("formOrder").get("campaign").get("name"))
        await bot.send_message(chat_id=user_id, text=text,  reply_markup=await inline.menu_new_post(),
                               disable_web_page_preview=True)

    async def _upload_post(self):
        buttons = PostModel(order_id=self.__data.get("formOrder").get("campaign").get("order_id"),
                            buttons=self.__data.get("formOrder").get("campaign").get("BUTTONS", ""))
        comment = PostModel(order_id=self.__data.get("formOrder").get("campaign").get("order_id"),
                            comment=self.__data.get("formOrder").get("campaign").get("comment", ""))
        text = PostModel(order_id=self.__data.get("formOrder").get("campaign").get("order_id"),
                         text=self.__data.get("formOrder").get("campaign").get("post").get("caption", ""))
        await fastapi.upload_buttons(json=buttons, token=self.__data.get("token"))
        await fastapi.upload_comment(json=comment, token=self.__data.get("token"))
        await fastapi.upload_text(json=text, token=self.__data.get("token"))

        if self.__data.get("formOrder").get("campaign").get("post", {}).get("file_id") is not None:
            type_file = self.__data.get("formOrder").get("campaign").get("post").get("type")
            file_id = self.__data.get("formOrder").get("campaign").get("post").get("file_id", "")
            json = PostModel(file_id=file_id, type_file=type_file,
                             order_id=self.__data.get("formOrder").get("campaign").get("order_id"))
            await fastapi.sender(json=json, token=self.__data.get("token"))

        if self.__data.get("formOrder").get("campaign").get("media", {}).get("file_id") is not None:
            type_file = "document"
            file_id = self.__data.get("formOrder").get("campaign").get("media").get("file_id", "")
            json = PostModel(file_id=file_id, type_file=type_file,
                             order_id=self.__data.get("formOrder").get("campaign").get("order_id"))

            await fastapi.sender(json=json, token=self.__data.get("token"))

        json = await func.form_order(data=self.__data)
        channels_response = await fastapi.add_channels(json=json, token=self.__data.get("token"))
        channels_response = channels_response.get("channels")
        return channels_response

