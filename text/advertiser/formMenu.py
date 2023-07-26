from string import Template
from aiogram.utils.markdown import hlink
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class FormMenuAdvertiser:
    def __init__(self, language: str):
        self.__Lang: Model = Txt.language[language]

    async def main(self):
        text = Template('$main\n\n'
                        '👉$text1')
        text = text.substitute(main=self.__Lang.start.main,
                               text1=hlink(url=self.__Lang.url.advertiser.how_to_use,
                                           title=self.__Lang.information.how_to_use))
        return text

    async def how_to_use(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Lang.url.advertiser.how_to_use,
                                           title=self.__Lang.information.how_to_use))
        return text

    async def about_us(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Lang.url.advertiser.about_us,
                                           title=self.__Lang.information.about_us))
        return text
