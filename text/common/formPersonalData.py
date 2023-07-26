from string import Template

from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class FormPersonalData:

    def __init__(self, data: dict):
        self.__data = data
        self.__Lang: Model = Txt.language[self.__data.get('lang')]

    async def menu_personal_data(self):
        text = Template("<b>$account:</b> $account_user\n\n"
                        "$choose")
        text = text.substitute(account=self.__Lang.personalData.common.account, account_user=self.__data.get("email"),
                               choose=self.__Lang.personalData.common.choose)
        return text

    async def menu_start(self):
        text = Template("<b>$account:</b> $account_user\n\n"
                        "$start")
        text = text.substitute(account=self.__Lang.personalData.common.account, account_user=self.__data.get("email"),
                               start=self.__Lang.personalData.common.start)
        return text
