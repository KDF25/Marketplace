from config import bot, moderation_chat_id
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi
from text.fuction.function import TextFunc
from text.group.formModeration import FormModerationGroup
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class OnModerationGroup:

    async def start(self):
        status, channels = await fastapi.get_on_moderation()
        Lang: Model = Txt.language["rus"]
        if status == 200 and len(channels) != 0:
            await self._get_all_channels(channels=channels)
        elif status == 200 and len(channels) == 0:
            await bot.send_message(text=Lang.alert.group.nonModeration, chat_id=moderation_chat_id)
        else:
            await bot.send_message(text=Lang.alert.common.error, chat_id=moderation_chat_id)

    async def _get_all_channels(self, channels: list):
        for channel in channels:
            await self._get_channel(data=channel)

    async def _get_channel(self, data: dict):
        form, inline = await self._prepare(data=data)
        await self._send(form=form, inline=inline)

    @staticmethod
    async def _prepare(data: dict):
        form = FormModerationGroup(data=data, language="rus")
        inline = InlineGroupUser(language="rus", enter_id=data.get("id"))
        return form, inline

    @staticmethod
    async def _send(form, inline):
        await bot.send_message(chat_id=moderation_chat_id, text=await form.menu_on_moderation(),
                               reply_markup=await inline.menu_moderation(), disable_web_page_preview=True)


