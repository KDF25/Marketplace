import datetime
from string import Template


from text.language.main import Text_main

Txt = Text_main()


class FormRegistration:

    def __init__(self, data: dict):
        self.__data = data
        self.__Lang = Txt.language[self.__data.get('lang')]

    async def menu_code(self):
        text = Template("$email\n"
                        "<b>$userEmail</b>\n\n"
                        "$code")
        text = text.substitute(email=self.__Lang.registration.common.email, userEmail=self.__data.get('email'),
                               code=self.__Lang.registration.common.code)
        return text

