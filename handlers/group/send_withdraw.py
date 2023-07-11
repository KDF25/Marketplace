from config import bot, moderation_chat_id
from keyboards.inline.group.user import InlineGroupUser
from looping import fastapi
from model.wallet import WalletModel
from text.common.formEntityData import FormEntityData
from text.common.formIndividualData import FormIndividualData
from text.common.formSelfEmployedAccountData import FormSelfEmployedAccountData
from text.common.formSelfEmployedCardData import FormSelfEmployedCardData
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class SendWithdraw:

    def __init__(self, data: dict, type_legal:str):
        self.__form = None
        self.__amount = None
        self.__data = data
        self.__type_legal = type_legal

    async def start(self):
        await self._prepare()
        await self._withdraw()
        await self._send()

    async def _prepare(self):
        if self.__type_legal == "entity":
            self.__type_legal = "entity"
            self.__amount = self.__data.get('entity').get("cash")
            self.__form = FormEntityData(data=self.__data.get("entity"), language="rus")
        elif self.__type_legal == "individual":
            self.__type_legal = "individual"
            self.__amount = self.__data.get('individual').get("cash")
            self.__form = FormIndividualData(data=self.__data.get("individual"), language="rus")
        elif self.__type_legal == "selfEmployedCard":
            self.__type_legal = "self_employed_transit"
            self.__amount = self.__data.get('selfEmployedCard').get("cash")
            self.__form = FormSelfEmployedCardData(data=self.__data.get("selfEmployedCard"), language="rus")
        elif self.__type_legal == "selfEmployedAccount":
            self.__type_legal = "self_employed"
            self.__amount = self.__data.get('selfEmployedAccount').get("cash")
            self.__form = FormSelfEmployedAccountData(data=self.__data.get("selfEmployedAccount"), language="rus")

    async def _withdraw(self):
        json = WalletModel(type_legal=self.__type_legal, amount=self.__amount)
        response = await fastapi.withdraw(json=json, token=self.__data.get("token"))
        self.__journal_id = response.get("journal_id")

    async def _send(self):
        inline = InlineGroupUser(language="rus", enter_id=self.__journal_id)
        await bot.send_message(chat_id=moderation_chat_id, text=await self.__form.menu_group(),
                               reply_markup=await inline.menu_withdraw())


