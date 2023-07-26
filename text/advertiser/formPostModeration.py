from string import Template

from aiogram.utils.markdown import hlink

from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormPostModeration:

    def __init__(self, language: str, data: dict = None):
        self.__data = data
        self.__Lang: Model = Txt.language[language]
        self.__accommodation = ""
        self.__price = 0
        self.__all_subscribers = 0

    async def _unpack_channel(self):
        self.__platform = self.__data.get("area_name")
        self.__name = self.__data.get("order_name")
        self.__url = self.__data.get("area_url")
        self.__post_url = self.__data.get('post_url')
        self.__date = self.__data.get("date")
        self.__accommodation = self.__data.get("accommodation")
        self.__time = await func.repack_time(data=self.__data.get("publish_times"))
        self.__time = await func.sort_time(time=self.__time)
        self.__price = await func.int_to_str(num=self.__data.get("price"))
        self.__comment = f"<b>{self.__Lang.formOrder.blogger.comment}:</b> {self.__data.get('comment')}\n\n" \
            if self.__data.get('comment') is not None and len(self.__data.get('comment')) != 0 else ""

    async def menu_accept(self):
        await self._unpack_channel()
        text = Template("$accept1 $platform $accept2\n\n"
                        "<b>$cash:</b> $price $sum")
        text = text.substitute(accept1=self.__Lang.postModeration.blogger.accept1,
                               platform=hlink(url=self.__url, title=self.__platform),
                               accept2=self.__Lang.postModeration.blogger.accept2,
                               cash=self.__Lang.postModeration.blogger.cash, price=self.__price,
                               sum=self.__Lang.postModeration.blogger.sum)
        return text

    async def menu_reject(self):
        await self._unpack_channel()
        text = Template("$reject\n\n"
                        "$comment"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$post: $post_url\n\n")
        text = text.substitute(reject=self.__Lang.postModeration.blogger.reject,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time, comment=self.__comment,
                               post=self.__Lang.formOrder.blogger.post, post_url=self.__post_url,)
        return text

    async def menu_moderation(self):
        await self._unpack_channel()
        text = Template("$reject\n\n"
                        "$comment"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$post: $post_url\n\n")
        text = text.substitute(reject=self.__Lang.postModeration.blogger.reject2,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time, comment=self.__comment,
                               post=self.__Lang.formOrder.blogger.post, post_url=self.__post_url,)
        return text

    async def menu_favor_blogger_blogger(self):
        await self._unpack_channel()
        text = Template("$blogger\n\n"
                        "<i>$apology</i>\n\n"                        
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(blogger=self.__Lang.postModeration.group.blogger.moderation_blogger,
                               apology=self.__Lang.postModeration.group.blogger.apology,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time, comment=self.__comment)
        return text

    async def menu_favor_blogger_advertiser(self):
        await self._unpack_channel()
        text = Template("$blogger\n\n"
                        "<i>$reminder</i>\n\n"                        
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(blogger=self.__Lang.postModeration.group.advertiser.moderation_blogger,
                               reminder=self.__Lang.postModeration.group.blogger.reminder,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time, comment=self.__comment)
        return text

    async def menu_favor_advertiser_advertiser(self):
        await self._unpack_channel()
        text = Template("$advertiser\n\n"
                        "<i>$apology</i>\n\n"                        
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(advertiser=self.__Lang.postModeration.group.advertiser.moderation_advertiser,
                               apology=self.__Lang.postModeration.group.advertiser.apology,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time, comment=self.__comment)
        return text

    async def menu_favor_advertiser_blogger(self):
        await self._unpack_channel()
        text = Template("$advertiser\n\n"
                        "<i>$reminder</i>\n\n"                        
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(advertiser=self.__Lang.postModeration.group.blogger.moderation_advertiser,
                               reminder=self.__Lang.postModeration.group.advertiser.reminder,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time, comment=self.__comment)
        return text



