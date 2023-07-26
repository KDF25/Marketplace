from string import Template
from typing import Union

from aiogram.utils.markdown import hlink

from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormPost:

    def __init__(self, language: str, data: dict = None):
        self.__data = data
        self.__Lang: Model = Txt.language[language]

    async def menu_post(self, comment: Union[str, int], caption: Union[str, int]):
        if caption is None and comment is None:
            text = ""
        elif caption is None and comment is not None:
            text = Template("$task: $comment")
            text = text.substitute(task=self.__Lang.formOrder.task, comment=comment)
        elif comment is None:
            text = Template("$caption")
            text = text.substitute(caption=caption)
        else:
            text = Template("$caption\n\n$task: $comment")
            text = text.substitute(caption=caption, task=self.__Lang.formOrder.task, comment=comment)
        return text

    async def menu_post_moderation(self):
        await self._unpack_channel()
        text = Template("$post_review\n\n"
                        "<b>$post:</b> $post_url"
                        "<b>$platform:</b> $title"
                        "<b>$campaign:</b> $campaign_name\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "<b>$comment:</b> $comment_post\n\n"
                        "$postCheck")
        text = text.substitute(completed=self.__Lang.formOrder.blogger.completed,
                               cash=self.__Lang.formOrder.blogger.cash,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__name),
                               campaign=self.__Lang.formOrder.blogger.name, campaign_name=self.__campaign,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__Lang.formOrder.blogger.comment, comment_post=self.__comment,
                               postCheck=self.__Lang.newOrder.advertiser.postCheck)
        return text

    async def _unpack_channel(self):
        self.__name = self.__data.get("name")
        self.__url = self.__data.get("url")
        self.__date = self.__data.get("date")
        self.__time = await func.sort_time(time=self.__data.get("time"))

        for accommodation in self.__data.get('area_accommodation'):
            if accommodation.get("id") in self.__data.get('current_accommodation'):
                self.__accommodation = accommodation.get("accommodation")
                self.__price = accommodation.get("price")