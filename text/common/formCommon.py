import datetime
from math import ceil
from string import Template

from datetime_now import dt_now
from text.language.main import Text_main
from text.fuction.function import TextFunc
from aiogram.utils.markdown import hlink

Txt = Text_main()
func = TextFunc()


class FormCommon:

    def __init__(self, language: str):
        self.__Lang = Txt.language[language]

    async def menu_rules(self):
        text = Template("$text1 $text2 $text3")
        text = text.substitute(text1=self.__Lang.registration.common.rules1,
                               text2=hlink(url=self.__Lang.url.common.rules,
                                           title=self.__Lang.registration.common.rules2),
                               text3=self.__Lang.registration.common.rules3)
        return text

    async def _rules(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Lang.url.driver.rules,
                                           title=self.__Lang.questions.registration.rules))
        return text

    async def _how_to_use(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Lang.url.driver.how_to_use,
                                           title=self.__Lang.questions.registration.how_to_use))
        return text

    async def finish(self):
        form = Template("<b>$id</b>: $driver_id\n"
                        "<b>$money</b>: $driver_money $sum\n\n"
                        "$congratulation\n\n"
                        "👉 $how_to_use\n"
                        "👉 $rules\n\n"
                        "<i>$online</i>")
        form = form.substitute(id=self.__Lang.personal_cabinet.id, driver_id=self.__data.get('user_id'),
                               money=self.__Lang.personal_cabinet.wallet, sum=self.__Lang.symbol.sum,
                               driver_money=await func.int_to_str(num=Txt.money.wallet.wallet),
                               congratulation=self.__Lang.personal_cabinet.congratulation,
                               how_to_use=await self._how_to_use(), rules=await self._rules(),
                               online=self.__Lang.personal_cabinet.online)
        return form

