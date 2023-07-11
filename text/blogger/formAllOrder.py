from math import ceil
from string import Template
from typing import Union

from aiogram.utils.markdown import hlink

from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FormAllOrderBlogger:

    def __init__(self, language: str, data: dict = None):
        self.__data = data
        self.__Lang = Txt.language[language]
        self.__accommodation = ""
        self.__price = 0
        self.__all_subscribers = 0

    async def menu_all_orders(self):
        text = Template("<b>$expects:</b> $expects_num\n"
                        "<b>$active:</b> $active_num\n"
                        "<b>$completed:</b> $completed_num\n\n"
                        "$choose")
        text = text.substitute(expects=self.__Lang.allOrder.expects, expects_num=self.__data.get("wait"),
                               active=self.__Lang.allOrder.active, active_num=self.__data.get("active"),
                               completed=self.__Lang.allOrder.completed, completed_num=self.__data.get("completed"),
                               choose=self.__Lang.allOrder.choose)
        return text

    async def menu_platform(self):
        text = Template("<b>$platform:</b> $title\n"
                        "$choose")
        text = text.substitute(platform=self.__Lang.allOrder.platform,
                               title=hlink(url=self.__data.get("url"), title=self.__data.get("name")),
                               choose=self.__Lang.allOrder.choose)
        return text

    async def menu_expects(self):
        text = Template("<b>$platform:</b> $title\n"
                        "$expects 👇 ")
        text = text.substitute(platform=self.__Lang.allOrder.platform,
                               title=hlink(url=self.__data.get("url"), title=self.__data.get("name")),
                               expects=self.__Lang.allOrder.expects)
        return text

    async def menu_active(self):
        text = Template("<b>$platform:</b> $title\n"
                        "$active 👇 ")
        text = text.substitute(platform=self.__Lang.allOrder.platform,
                               title=hlink(url=self.__data.get("url"), title=self.__data.get("name")),
                               active=self.__Lang.allOrder.active)
        return text

    async def menu_completed(self):
        text = Template("<b>$platform:</b> $title\n"
                        "$completed 👇 ")
        text = text.substitute(platform=self.__Lang.allOrder.platform,
                               title=hlink(url=self.__data.get("url"), title=self.__data.get("name")),
                               completed=self.__Lang.allOrder.completed)
        return text

