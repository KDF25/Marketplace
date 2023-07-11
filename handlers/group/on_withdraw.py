from config import bot, moderation_chat_id
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi
from text.fuction.function import TextFunc
from text.group.formWithdraw import FormWithdrawGroup
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class OnWithdrawGroup:

    async def start(self):
        status, json = await fastapi.get_on_withdraw()
        Lang = Txt.language["rus"]
        if status == 200 and len(json.get("journal")) != 0:
            withdrawal = json.get("journal")
            await self._get_all_withdraw(withdrawal=withdrawal)
        elif status == 200 and len(json.get("journal")) == 0:
            await bot.send_message(text=Lang.alert.group.nonWithdraw, chat_id=moderation_chat_id)
        else:
            await bot.send_message(text=Lang.alert.common.error, chat_id=moderation_chat_id)

    async def _get_all_withdraw(self, withdrawal: list):
        for withdraw in withdrawal:
            await self._get_withdraw(data=withdraw)

    async def _get_withdraw(self, data: dict):
        form, inline = await self._prepare(data=data)
        await self._send(form=form, inline=inline)

    @staticmethod
    async def _prepare(data: dict):
        form = FormWithdrawGroup(data=data, language="rus")
        inline = InlineGroupUser(language="rus", enter_id=data.get("withdrawal_data").get("journal_id"))
        return form, inline

    @staticmethod
    async def _send(form, inline):
        await bot.send_message(chat_id=moderation_chat_id, text=await form.menu_on_withdraw(),
                               reply_markup=await inline.menu_withdraw(), disable_web_page_preview=True)
