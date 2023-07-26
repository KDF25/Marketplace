from string import Template

from aiogram.utils.markdown import hlink

from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormNewOrder:

    def __init__(self, language: str, data: dict = None):
        self.__data = data
        self.__Lang: Model = Txt.language[language]

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
        self.__comment = f"<b>{self.__Lang.formOrder.blogger.comment}:</b> {self.__data.get('comment')}" \
            if self.__data.get('comment') is not None and len(self.__data.get('comment')) != 0 else ""

    async def menu_send_blogger(self):
        await self._unpack_channel()
        text = Template("$new $title\n\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment\n"
                        "$attention")
        text = text.substitute(new=self.__Lang.formOrder.blogger.new,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__comment, attention=self.__Lang.formOrder.blogger.attention)
        return text

    async def menu_reject(self):
        await self._unpack_channel()
        text = Template("$reject\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(reject=self.__Lang.newOrder.advertiser.reject,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__comment, attention=self.__Lang.formOrder.blogger.attention)
        return text

    async def menu_accept_advertiser(self):
        await self._unpack_channel()
        text = Template("$accept\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment\n\n"
                        "$info")
        text = text.substitute(accept=self.__Lang.newOrder.advertiser.accept,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__comment, info=self.__Lang.newOrder.advertiser.info)
        return text

    async def menu_accept(self):
        await self._unpack_channel()
        text = Template("<b>$accept</b>\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(accept=self.__Lang.newOrder.blogger.accept_project,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__comment)
        return text

    async def menu_completed(self):
        await self._unpack_channel()
        text = Template("<b>$accept_advertiser</b>\n\n"
                        "<b>$cash:</b> $price_post $sum\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(accept_advertiser=self.__Lang.newOrder.blogger.accept_advertiser,
                               cash=self.__Lang.formOrder.blogger.cash,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__comment)
        return text

    async def menu_send_advertiser(self, message_text):
        await self._unpack_channel()
        text = Template("$message\n\n"
                        "<i>«$message_text»</i>\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "$comment")
        text = text.substitute(message=self.__Lang.newOrder.advertiser.message, message_text=message_text,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__comment)
        return text

    async def menu_check_post(self):
        await self._unpack_channel()
        text = Template("$post_review\n\n"
                        "<b>$post:</b> $post_url\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "<b>$comment:</b> $comment_post\n\n"
                        "$postCheck")
        text = text.substitute(post_review=self.__Lang.formOrder.blogger.post_review,
                               post=self.__Lang.formOrder.blogger.post, post_url=self.__post_url,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__Lang.formOrder.blogger.comment, comment_post=self.__comment,
                               postCheck=self.__Lang.newOrder.advertiser.postCheck)
        return text

    async def menu_review_post(self):
        await self._unpack_channel()
        text = Template("$post_review\n\n"
                        "<b>$post:</b> $post_url\n\n"
                        "<b>$platform:</b> $title\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "<b>$comment:</b> $comment_post")
        text = text.substitute(post_review=self.__Lang.formOrder.blogger.post_review,
                               post=self.__Lang.formOrder.blogger.post, post_url=self.__post_url,
                               platform=self.__Lang.formOrder.blogger.platform,
                               title=hlink(url=self.__url, title=self.__platform),
                               name=self.__Lang.formOrder.blogger.name, name_post=self.__name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=self.__price,
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__Lang.formOrder.blogger.comment, comment_post=self.__comment )
        return text



