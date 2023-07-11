from config import bot, moderation_chat_id
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi, pg
from text.blogger.formPlatform import FormPlatform
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class SendModeration:

    def __init__(self, data: dict, user_id: int):
        self.__user_id = user_id
        self.__data = data

    async def send_group(self):
        await self._add_platform()
        await self._prepare()
        await self._send()

    async def _add_platform(self):
        self.__data.get("area")["client_id"] = await pg.select_client_id(user_id=self.__user_id)
        json = await func.add_platform(data=self.__data.get("area"))
        response = await fastapi.moderation(json=json, token=self.__data.get('token'))
        self.__area_id = response.get("area_id")

    async def _prepare(self):
        self.__form = FormPlatform(data=self.__data.get("area"), language="rus")
        self.__inline = InlineGroupUser(language="rus", enter_id=self.__area_id)

    async def _send(self):
        await bot.send_message(chat_id=moderation_chat_id, text=await self.__form.menu_group(),
                               reply_markup=await self.__inline.menu_moderation(), disable_web_page_preview=True)

