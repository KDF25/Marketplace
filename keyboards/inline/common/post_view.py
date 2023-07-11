import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from looping import fastapi
from model.platform import Params
from text.language.main import Text_main
import calendar


Txt = Text_main()


class InlinePostView():

    def __init__(self, language: str, url_buttons: dict):
        self.__Lang = Txt.language[language]
        self.__url_buttons = url_buttons
        self.__markup = None

    async def menu_post(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        if self.__url_buttons is not None:
            await self._url_buttons()
        return self.__markup

    async def _url_buttons(self):
        old_row = 0
        for buttons in self.__url_buttons:
            row = buttons.get("row_id")
            print(row)
            text = buttons.get("name")
            url = buttons.get("link")
            b = InlineKeyboardButton(text=text, url=url.strip())
            if row != old_row:
                self.__markup.add(b)
            else:
                self.__markup.insert(b)
            old_row = row
