from string import Template
from typing import Union

from aiogram.utils.markdown import hlink

from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormOrder:

    def __init__(self, language: str, data: dict = None):
        self.__all_views = 0
        self.__data = data
        self.__Lang: Model = Txt.language[language]
        self.__accommodation = ""
        self.__price = 0
        self.__all_subscribers = 0

    async def menu_post(self, comment: Union[str, int], caption: Union[str, int]):
        if caption is None and comment is None:
            text = ""
        elif caption is None and comment is not None:
            text = Template("<b>$task:</b> $comment")
            text = text.substitute(task=self.__Lang.formOrder.task, comment=comment)
        elif comment is None:
            text = Template("$caption")
            text = text.substitute(caption=caption)
        else:
            text = Template("$caption\n\n<b>$task:</b> $comment")
            text = text.substitute(caption=caption, task=self.__Lang.formOrder.task, comment=comment)
        return text

    async def menu_form_order(self):
        await self._unpack()
        text = Template("$about\n\n"
                        "<b>$category:</b> <i>$category_business</i>\n"
                        "<b>$sex:</b> <i>$sex_platform</i>\n"
                        "<b>$lang:</b> <i>$lang_platform</i>\n"
                        "<b>$age:</b> <i>$age_platform</i>\n"
                        "<b>$region:</b> <i>$region_platform</i>\n"
                        "<b>$network:</b> <i>$all_network</i>\n\n"
                        "$select")
        text = text.substitute(about=self.__Lang.formOrder.about,
                               category=self.__Lang.platform.blogger.form.category,
                               category_business=self.__category_business,
                               sex=self.__Lang.formOrder.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.formOrder.form.lang, lang_platform=self.__lang_platform,
                               age=self.__Lang.formOrder.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.formOrder.form.region, region_platform=self.__region_platform,
                               network=self.__Lang.formOrder.form.network, all_network=self.__all_network,
                               select=self.__Lang.formOrder.select)
        return text

    async def _unpack(self):
        self.__category_business = await func.join(parameters=self.__data.get("category").get("values"))
        self.__sex_platform = self.__data.get("sex_value", "...")
        self.__lang_platform = await func.join(parameters=self.__data.get("platformLang").get("values"))
        self.__age_platform = await func.join(parameters=self.__data.get("age").get("values"))
        self.__all_network = await func.join(parameters=self.__data.get("network").get("values"))
        await self._region()

    async def _region(self):
        max_len = 12
        region_len = len(self.__data.get("regions").get("values"))
        if max_len != region_len:
            self.__region_platform = await func.join(parameters=self.__data.get("regions").get("values"))
        else:
            self.__region_platform = self.__Lang.platform.blogger.wholeCountry

    async def menu_parameters(self):
        await self._unpack()
        text = Template("$audience\n\n"
                        "<b>$sex:</b> <i>$sex_platform</i>\n"
                        "<b>$lang:</b> <i>$lang_platform</i>\n"
                        "<b>$age:</b> <i>$age_platform</i>\n"
                        "<b>$region:</b> <i>$region_platform</i>\n\n"
                        "$select")
        text = text.substitute(audience=self.__Lang.platform.blogger.change.audience,
                               sex=self.__Lang.platform.blogger.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.platform.blogger.form.lang,lang_platform=self.__lang_platform,
                               age=self.__Lang.platform.blogger.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.platform.blogger.form.region, region_platform=self.__region_platform,
                               select=self.__Lang.formOrder.select)
        return text

    async def menu_category(self):
        await self._category()
        text = Template("<b>$category:</b> <i>$category_business</i>\n\n"
                        "$select")
        text = text.substitute(category=self.__Lang.formOrder.form.category, category_business=self.__category_business,
                               select=self.__Lang.formOrder.form.select_business)
        return text

    async def _category(self):
        self.__category_business = await func.join(parameters=self.__data.get("category").get("values"))

    async def menu_all_platform(self):
        await self._unpack()
        await self._all_platform()
        text = Template("<b>$category:</b> <i>$category_business</i>\n"
                        "<b>$network:</b> <i>$all_network</i>\n"
                        "<b>$sex:</b> <i>$sex_platform</i>\n"
                        "<b>$age:</b> <i>$age_platform</i>\n"
                        "<b>$lang:</b> <i>$lang_platform</i>\n"
                        "<b>$region:</b> <i>$region_platform</i>\n\n"
                        "$allPlatform")
        text = text.substitute(category=self.__Lang.platform.blogger.form.category,
                               category_business=self.__category_business,
                               sex=self.__Lang.formOrder.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.formOrder.form.lang, lang_platform=self.__lang_platform,
                               age=self.__Lang.formOrder.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.formOrder.form.region, region_platform=self.__region_platform,
                               network=self.__Lang.formOrder.form.network, all_network=self.__all_network,
                               allPlatform=self.__all_platform)
        return text

    async def _all_platform(self):
        self.__all_platform = ''
        for platform in self.__data.get("channels").get('platformList'):
            self.__title = platform.get("name")
            self.__url = platform.get("url")
            self.__rate = "—"
            # self.__subscribes = await func.int_to_str(num=int(platform.get("subscribers") / 1000))
            self.__subscribes = round(platform.get('subscribers', 0) / 1000, 1)
            languages = [i.get('language')[0:2] for i in platform.get("area_language")]
            self.__languages = await func.join(parameters=languages)
            self.__views = round(platform.get('views', 0) / 1000, 1)
            self.__description = platform.get('description')
            self.__text_limit = "" if platform.get("text_limit") is None else \
                f"{self.__Lang.platform.blogger.form.symbol1} {platform.get('text_limit')} {self.__Lang.platform.blogger.form.symbol2}\n"
            await self._all_platform_accommodation(data=platform)
            await self._platform()
            self.__all_platform += self.__platform

    async def _all_platform_accommodation(self, data: dict):
        for accommodation in data.get("area_accommodation"):
            if accommodation.get("id") == self.__data.get("siteRequest").get("accommodation"):
                self.__price = accommodation.get("price")
                self.__accommodation = accommodation.get("accommodation")

    async def _platform(self):
        text = Template("$title\n"
                        "⭐ $rate | 👥<b>$subscribes</b> k | 👀 <b>$views</b> k\n"
                        "$accommodation — <b>$price</b> $sum\n\n")
        price = await func.int_to_str(num=self.__price)
        self.__platform = text.substitute(title=hlink(url=self.__url, title=self.__title), rate=self.__rate,
                                          subscribes=self.__subscribes, language=self.__languages,
                                          text_limit=self.__text_limit, views=self.__views,
                                          accommodation=self.__accommodation, price=price, sum=self.__Lang.formOrder.form.sum,
                                          description=self.__Lang.formOrder.form.description,
                                          description_platform=self.__description)

    async def menu_search_filters(self):
        await self._unpack()
        text = Template("<b>$category:</b> <i>$category_business</i>\n"
                        "<b>$sex:</b> <i>$sex_platform</i>\n"
                        "<b>$lang:</b> <i>$lang_platform</i>\n"
                        "<b>$age:</b> <i>$age_platform</i>\n"
                        "<b>$region:</b> <i>$region_platform</i>\n")
        text = text.substitute(category=self.__Lang.platform.blogger.form.category,
                               category_business=self.__category_business,
                               sex=self.__Lang.formOrder.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.formOrder.form.lang, lang_platform=self.__lang_platform,
                               age=self.__Lang.formOrder.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.formOrder.form.region, region_platform=self.__region_platform)
        return text

    async def menu_campaign_text(self):
        text = Template("<b>$campaignName</b>\n\n"
                        "$text\n\n"
                        "$text2\n\n")
        text = text.substitute(campaignName=self.__data.get("campaign").get("name"),
                               text=self.__Lang.formOrder.campaignText,
                               text2=hlink(url=self.__Lang.url.advertiser.how_to_use,
                                           title=self.__Lang.formOrder.campaignText2))
        return text

    async def menu_current_platform(self):
        await self._unpack_current_platform(data=self.__data)
        await self._current_accommodation(data=self.__data)
        text = Template("$title\n"
                        "⭐ $rate | 👥 <b>$subscribes</b> k | 👀 <b>$views</b> k | $language\n"
                        "<i>$text_limit</i>\n"
                        "$accommodation\n"
                        "<b>$description:</b> <i>$description_platform</i>\n\n")
        text = text.substitute(title=hlink(url=self.__url, title=self.__title), rate=self.__rate,views=self.__views,
                               text_limit=self.__text_limit, subscribes=self.__subscribes, language=self.__languages,
                               accommodation=self.__accommodation, description=self.__Lang.formOrder.form.description,
                               description_platform=self.__description)
        return text

    async def _unpack_current_platform(self, data: dict):
        self.__title = data.get("name")
        self.__url = data.get("url")
        self.__rate = "-"
        self.__subs = data.get("subscribers")
        self.__view = data.get('views', 0)
        self.__views = round(data.get('views', 0) / 1000, 1)
        self.__text_limit = "" if data.get("text_limit") is None else \
            f"{self.__Lang.platform.blogger.form.symbol1} {data.get('text_limit')} {self.__Lang.platform.blogger.form.symbol2}\n"
        # self.__subscribes = await func.int_to_str(num=int(data.get("subscribers") / 1000))
        self.__subscribes = round(data.get('subscribers', 0) / 1000, 1)
        languages = [i.get('language')[0:2] for i in data.get("area_language")]
        self.__languages = await func.join(parameters=languages)
        self.__description = data.get('description')

    async def _current_accommodation(self, data: dict):
        for accommodation in data.get('area_accommodation'):
            if accommodation.get("id") in data.get('current_accommodation'):
                text = Template("$accommodation — <b>$price</b> $sum\n")
                text = text.substitute(accommodation=accommodation.get("accommodation"),
                                       price=await func.int_to_str(accommodation.get("price")),
                                       sum=self.__Lang.formOrder.form.sum)
                self.__accommodation += text
                self.__price += accommodation.get("price")

    async def menu_basket(self):
        await self._unpack_basket()
        cost = await func.commission(price=self.__price)
        text = Template("<b>$basket</b>\n\n"
                        "$all_platform"
                        "$subscribers — $all_subscribers\n"
                        "$coverage — $all_coverage\n\n"
                        "$commission\n"
                        "<b>$cost — $all_cost $sum</b>")
        text = text.substitute(basket=self.__Lang.formOrder.basket.basket, all_platform=self.__all_platform,
                               subscribers=self.__Lang.formOrder.basket.subscribers, all_subscribers=self.__all_subscribers,
                               coverage=self.__Lang.formOrder.basket.coverage, all_coverage=self.__all_views,
                               commission=self.__Lang.formOrder.basket.commission, nds=self.__Lang.formOrder.basket.nds,
                               cost=self.__Lang.formOrder.basket.cost, sum=self.__Lang.formOrder.form.sum,
                               all_cost=await func.int_to_str(num=cost))

        return text

    async def _unpack_basket(self):
        self.__all_platform = ""
        for platform in self.__data.get("channels"):
            self.__accommodation = ""
            await self._unpack_current_platform(data=platform)
            await self._current_accommodation(data=platform)
            await self._basket()
            self.__all_subscribers += self.__subs
            self.__all_views += self.__view
        self.__all_subscribers = await func.int_to_str(num=self.__all_subscribers)
        self.__all_views = await func.int_to_str(num=self.__all_views)

    async def _basket(self):
        text = Template("$title\n"
                        "⭐$rate | 👥 <b>$subscribes</b> k | 👀 <b>$views</b> k\n"
                        "$accommodation\n")
        text = text.substitute(title=hlink(url=self.__url, title=self.__title), rate=self.__rate, views=self.__views,
                               subscribes=self.__subscribes, language=self.__languages, accommodation=self.__accommodation,
                               description=self.__Lang.formOrder.form.description,
                               description_platform=self.__description)
        self.__all_platform += text

    async def menu_last_preview(self, campaign_name: str):
        await self._unpack_last_preview()
        cost = self.__data.get("total_cost")
        text = Template("<b>$campaign_name</b>\n\n"
                        "$all_platform"
                        "$subscribers — $all_subscribers\n"
                        "$coverage — $all_coverage\n\n"
                        "$commission\n"
                        "<b>$cost — $all_cost $sum</b>")
        text = text.substitute(campaign_name=campaign_name, all_platform=self.__all_platform,
                               subscribers=self.__Lang.formOrder.basket.subscribers, all_subscribers=self.__all_subscribers,
                               coverage=self.__Lang.formOrder.basket.coverage, all_coverage=self.__all_views,
                               commission=self.__Lang.formOrder.basket.commission, nds=self.__Lang.formOrder.basket.nds,
                               cost=self.__Lang.formOrder.basket.cost, sum=self.__Lang.formOrder.form.sum,
                               all_cost=await func.int_to_str(num=cost))

        return text

    async def _unpack_last_preview(self):
        self.__all_platform = ""
        for platform in self.__data.get("channels"):
            self.__accommodation = ""
            await self._unpack_current_platform(data=platform)
            await self._current_accommodation(data=platform)
            self.__date = platform.get('date')
            self.__time = await func.sort_time(platform.get('time'))
            await self._last_preview()
            self.__all_subscribers += self.__subs
            self.__all_views += self.__view
        self.__all_subscribers = await func.int_to_str(num=self.__all_subscribers)
        self.__all_views = await func.int_to_str(num=self.__all_views)

    async def _last_preview(self):
        text = Template("$title\n"
                        "⭐$rate | 👥 <b>$subscribes</b> k | 👀 <b>$views</b> k\n"
                        "🗓$date , ⏰$time\n"
                        "$accommodation\n")
        text = text.substitute(title=hlink(url=self.__url, title=self.__title), rate=self.__rate,
                               subscribes=self.__subscribes, language=self.__languages, views=self.__views,
                               date=self.__date, time=self.__time, accommodation=self.__accommodation,
                               description=self.__Lang.formOrder.form.description,
                               description_platform=self.__description)
        self.__all_platform += text

    async def menu_send_blogger(self, comment: Union[str, int], name: Union[str, int]):
        await self._unpack_channel()
        text = Template("$new $title\n\n"
                        "<b>$name:</b> $name_post\n"
                        "<b>$accommodation:</b> $accommodation_post\n"
                        "<b>$price:</b> $price_post $sum\n"
                        "<b>$date:</b> $date_post\n"
                        "<b>$time:</b> $time_post\n"
                        "<b>$comment:</b> $comment_post\n\n"
                        "$attention")
        text = text.substitute(new=self.__Lang.formOrder.blogger.new, title=hlink(url=self.__url, title=self.__name),
                               name=self.__Lang.formOrder.blogger.name, name_post=name,
                               accommodation=self.__Lang.formOrder.blogger.accommodation,
                               accommodation_post=self.__accommodation, sum=self.__Lang.formOrder.blogger.sum,
                               price=self.__Lang.formOrder.blogger.price, price_post=await func.int_to_str(num=self.__price),
                               date=self.__Lang.formOrder.blogger.date, date_post=self.__date,
                               time=self.__Lang.formOrder.blogger.time, time_post=self.__time,
                               comment=self.__Lang.formOrder.blogger.comment, comment_post=comment,
                               attention=self.__Lang.formOrder.blogger.attention)
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

    async def menu_calendar(self, campaign_name: str):
        text = Template("<b>$campaign_name</b>\n\n"
                        "$date")
        text = text.substitute(campaign_name=campaign_name, date=self.__Lang.formOrder.date)
        return text

    async def menu_all_dates(self, campaign_name: str):
        text = Template("<b>$campaign_name</b>\n\n"
                        "$all_dates")
        text = text.substitute(campaign_name=campaign_name, all_dates=self.__Lang.formOrder.all_dates)
        return text

    async def menu_time(self, campaign_name: str):
        text = Template("<b>$campaign_name</b>\n\n"
                        "$time")
        text = text.substitute(campaign_name=campaign_name, time=self.__Lang.formOrder.time)
        return text

