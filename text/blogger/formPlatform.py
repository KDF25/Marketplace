import datetime
from math import ceil
from string import Template
from aiogram.utils.markdown import hlink
from random import randint

from datetime_now import dt_now
from looping import fastapi
from model.platform import GetValue
from text.language.main import Text_main
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FormPlatform:

    def __init__(self, language: str, formats=None, data: dict = None):
        self.__url = None
        self.__title = None
        self.__rate = None
        self.__subscribes = None
        self.__views = None
        self.__languages = None
        self.__all_platform = ""
        self.__data = data
        self.__formats = formats
        self.__Lang = Txt.language[language]

    async def platform_reject(self):
        text = Template("$alert\n\n"
                        "<b>$reason:</b> $platform_reason\n\n"
                        "$next —  <b>$date</b>")
        text = text.substitute(alert=self.__Lang.alert.blogger.platformReject,
                               reason=self.__Lang.group.moderation.user.reason,
                               platform_reason=self.__data.get("reason"),
                               next=self.__Lang.platform.blogger.nextTime,
                               date=self.__data.get("value"))
        return text

    async def platform_ban(self):
        text = Template("$alert\n\n"
                        "<b>$reason:</b> $platform_reason")
        text = text.substitute(alert=self.__Lang.alert.blogger.platformBan,
                               reason=self.__Lang.group.moderation.user.reason,
                               platform_reason=self.__data.get("reason"))
        return text

    async def menu_telegram_verification(self, code):
        text = Template("$add_platform — <code><b>$code</b></code>\n\n"
                        "$check")
        text = text.substitute(add_platform=self.__Lang.platform.blogger.checkTelegram1, code=code,
                               check=self.__Lang.platform.blogger.checkTelegram2)
        return text

    async def menu_price(self):
        await self._formats()
        text = Template("<b>$formats</b>\n\n"
                        "$price")
        text = text.substitute(formats=self.__formats, price=self.__Lang.platform.blogger.price)
        return text

    async def _formats(self):
        for accommodation in self.__data:
            if int(accommodation['id']) == int(self.__formats):
                self.__formats = accommodation['name']
                break

    async def menu_formats(self):
        await self._all_price(accommodations=self.__data)
        text = Template("$add\n"
                        "$all_price\n\n"
                        "$format")
        text = text.substitute(add=self.__Lang.platform.blogger.add_format,
                               all_price=self.__price_platform, format=self.__Lang.platform.blogger.format)
        return text

    async def _all_price(self, accommodations: dict):
        self.__price_platform = ""
        for accommodation in accommodations:
            if accommodation.get("price") is not None:
                self.__price = accommodation.get("price")
                self.__accommodation = accommodation.get("name")
                await self._price()

    async def _price(self):
        text = Template("\n$format - <b>$price</b> $sum")
        self.__text = text.substitute(format=self.__accommodation, price=await func.int_to_str(num=self.__price),
                                      sum=self.__Lang.symbol.sum)
        self.__price_platform += self.__text

    async def menu_platform(self):
        await self._unpack_platform()
        text = Template("$check\n\n"
                        "<b>$title_platform</b>\n"
                        "$type_platform - $url_platform\n\n"
                        "<b>$description:</b> $description_platform\n\n"
                        "<b>$category:</b> $category_platform\n"
                        "<b>$sex:</b> $sex_platform\n"
                        "<b>$lang:</b> $lang_platform\n"
                        "<b>$age:</b> $age_platform\n"
                        "<b>$region:</b> $region_platform\n"
                        "$symbol_platform\n"
                        "<b>$price:</b>\n $price_platform\n")
        text = text.substitute(check=self.__Lang.platform.blogger.form.check,
                               type_platform=self.__type_platform,
                               title_platform=self.__title_platform, url_platform=self.__url_platform,
                               description=self.__Lang.platform.blogger.form.description,
                               description_platform=self.__description_platform,
                               category=self.__Lang.platform.blogger.form.category,
                               category_platform=self.__category_platform,
                               sex=self.__Lang.platform.blogger.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.platform.blogger.form.lang,lang_platform=self.__lang_platform,
                               age=self.__Lang.platform.blogger.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.platform.blogger.form.region, region_platform=self.__region_platform,
                               symbol_platform=self.__symbol_platform,  price=self.__Lang.platform.blogger.form.price,
                               price_platform=self.__price_platform)
        return text

    async def menu_change(self):
        await self._unpack_platform()
        text = Template("<b>$title_platform</b>\n"
                        "$type_platform - $url_platform\n\n"
                        "<b>$description:</b> $description_platform\n\n"
                        "<b>$category:</b> $category_platform\n"
                        "<b>$sex:</b> $sex_platform\n"
                        "<b>$lang:</b> $lang_platform\n"
                        "<b>$age:</b> $age_platform\n"
                        "<b>$region:</b> $region_platform\n"
                        "$symbol_platform\n"
                        "<b>$price:</b>\n $price_platform\n")
        text = text.substitute(type_platform=self.__type_platform,
                               title_platform=self.__title_platform, url_platform=self.__url_platform,
                               description=self.__Lang.platform.blogger.form.description,
                               description_platform=self.__description_platform,
                               category=self.__Lang.platform.blogger.form.category,
                               category_platform=self.__category_platform,
                               sex=self.__Lang.platform.blogger.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.platform.blogger.form.lang, lang_platform=self.__lang_platform,
                               age=self.__Lang.platform.blogger.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.platform.blogger.form.region, region_platform=self.__region_platform,
                               symbol_platform=self.__symbol_platform,  price=self.__Lang.platform.blogger.form.price,
                               price_platform=self.__price_platform)
        return text

    async def _unpack_platform(self):
        self.__type_platform = self.__data.get("platform").title()
        self.__title_platform = self.__data.get("name")
        self.__url_platform = self.__data.get("url")
        self.__description_platform = self.__data.get("description")
        self.__category_platform = self.__data.get("category").get('value')
        self.__sex_platform = self.__data.get("sex_value")
        self.__lang_platform = await func.join(parameters=self.__data.get("platformLang").get("values"))
        self.__age_platform = await func.join(parameters=self.__data.get("age").get("values"))
        await self._region()
        await self._symbol()
        await self._all_price(accommodations=self.__data.get('accommodation'))

    async def _symbol(self):
        if self.__data.get("symbol") is not None:
            text = Template("$symbol1 $symbol_platform $symbol2\n")
            self.__symbol_platform = text.substitute(symbol1=self.__Lang.platform.blogger.form.symbol1,
                                                     symbol_platform=self.__data.get("symbol"),
                                                     symbol2=self.__Lang.platform.blogger.form.symbol2)
        else:
            self.__symbol_platform = ""

    async def _region(self):
        max_len = 14
        # max_len = len(self.__data.get("regions").get("all_values"))
        region_len = len(self.__data.get("regions").get("values"))
        if max_len != region_len:
            self.__region_platform = await func.join(parameters=self.__data.get("regions").get("values"))
        else:
            self.__region_platform = self.__Lang.platform.blogger.wholeCountry

    async def menu_all_platform(self):
        await self._all_platform()
        text = Template("$platform:\n\n"
                        "$all_platform")
        text = text.substitute(platform=self.__Lang.platform.blogger.form.all_platform, all_platform=self.__all_platform)
        return text

    async def _all_platform(self):
        for platform in self.__data:
            self.__title = platform.get("name")
            self.__url = platform.get("url")
            self.__rate = "-"
            self.__subscribes = await func.int_to_str(num=ceil(platform.get("subscribers")/1000))
            self.__languages = await func.join(parameters=platform.get("platformLang").values())
            await self._platform()
            self.__all_platform += self.__platform

    async def _platform(self):
        text = Template("$title\n"
                        "⭐ $rate | 👥 $subscribes k | $language\n\n")
        self.__platform = text.substitute(title=hlink(url=self.__url, title=self.__title), rate=self.__rate,
                                          subscribes=self.__subscribes, language=self.__languages)

    async def menu_delete_end(self):
        text = Template("$delete_end\n\n" 
                        "<b>$platform:</b> $title")
        text = text.substitute(delete_end=self.__Lang.platform.blogger.delete_end,
                               platform=self.__Lang.platform.blogger.form.platform,
                               title=hlink(url=self.__data.get("url"), title=self.__data.get("name")))
        return text

    async def menu_parameters(self):
        await self._unpack_platform()
        text = Template("$audience\n\n"
                        "<b>$sex:</b> $sex_platform\n"
                        "<b>$lang:</b> $lang_platform\n"
                        "<b>$age:</b> $age_platform\n"
                        "<b>$region:</b> $region_platform\n")
        text = text.substitute(audience=self.__Lang.platform.blogger.change.audience,
                               sex=self.__Lang.platform.blogger.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.platform.blogger.form.lang,lang_platform=self.__lang_platform,
                               age=self.__Lang.platform.blogger.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.platform.blogger.form.region, region_platform=self.__region_platform)
        return text

    async def menu_group(self):
        await self._unpack_platform()
        date = datetime.datetime.strftime(dt_now.now(), "%d.%m.%Y")
        text = Template("<b>$request</b>\n"
                        "<b>$date_request:</b> $today\n\n"
                        "<b>$title_platform</b>\n"
                        "$type_platform - $url_platform\n\n"
                        "<b>$description:</b> $description_platform\n\n"
                        "<b>$category:</b> $category_platform\n"
                        "<b>$sex:</b> $sex_platform\n"
                        "<b>$lang:</b> $lang_platform\n"
                        "<b>$age:</b> $age_platform\n"
                        "<b>$region:</b> $region_platform\n"
                        "$symbol_platform\n"
                        "<b>$price:</b>\n $price_platform\n")
        text = text.substitute(request=self.__Lang.platform.blogger.request,
                               date_request=self.__Lang.platform.blogger.date_request,  today=date,
                               type_platform=self.__type_platform,
                               title_platform=self.__title_platform, url_platform=self.__url_platform,
                               description=self.__Lang.platform.blogger.form.description,
                               description_platform=self.__description_platform,
                               category=self.__Lang.platform.blogger.form.category,
                               category_platform=self.__category_platform,
                               sex=self.__Lang.platform.blogger.form.sex, sex_platform=self.__sex_platform,
                               lang=self.__Lang.platform.blogger.form.lang,lang_platform=self.__lang_platform,
                               age=self.__Lang.platform.blogger.form.age, age_platform=self.__age_platform,
                               region=self.__Lang.platform.blogger.form.region, region_platform=self.__region_platform,
                               symbol_platform=self.__symbol_platform,  price=self.__Lang.platform.blogger.form.price,
                               price_platform=self.__price_platform)
        return text








