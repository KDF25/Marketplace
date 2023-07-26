import datetime
from string import Template
from typing import Union

from aiogram.utils.markdown import hlink

from datetime_now import dt_now
from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormModerationGroup:

    def __init__(self, language: str, url: str = None, name: Union[int, str] = None, text: str = None, data: dict = None):
        self.__text = text
        self.__url = url
        self.__name = name
        self.__data = data
        self.__Lang: Model = Txt.language[language]

    async def menu_accept_user(self):
        text = Template("<b>$accept</b>\n\n"
                        "<b>$platform:</b> $name\n\n"
                        "$myPlatform")
        text = text.substitute(accept=self.__Lang.group.moderation.user.accept,
                               name=hlink(url=self.__url, title=self.__name),
                               platform=self.__Lang.group.moderation.user.platform,
                               myPlatform=self.__Lang.group.moderation.user.myPlatform)
        return text

    async def menu_reject_user(self):
        text = Template("$reject\n\n"
                        "<b>$platform:</b> $name\n\n"
                        "<b>$reason:</b> $text\n\n")
        text = text.substitute(reject=self.__Lang.group.moderation.user.reject,
                               name=hlink(url=self.__url, title=self.__name),
                               platform=self.__Lang.group.moderation.user.platform,
                               reason=self.__Lang.group.moderation.user.reason, text=self.__text)
        return text

    async def menu_on_moderation(self):
        await self._unpack_platform()
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
                               date_request=self.__Lang.platform.blogger.date_request,  today=self.__date,
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

    async def _unpack_platform(self):
        self.__date = self.__data.get("date", datetime.datetime.strftime(dt_now.now(), "%d.%m.%Y"))
        self.__type_platform = self.__data.get("type").get("type")
        self.__title_platform = self.__data.get("name")
        self.__url_platform = self.__data.get("url")
        self.__description_platform = self.__data.get("description")
        self.__category_platform = self.__data.get("category")
        self.__sex_platform = self.__data.get("sex_ratio").get("ratio")
        self.__lang_platform = str(', '.join((parameter.get("language")[0:3] for parameter in self.__data.get("area_language"))))
        self.__age_platform = str(', '.join((parameter.get("age") for parameter in self.__data.get("area_age"))))
        self.__symbol_platform = self.__data.get("text_limit", "")
        await self._region()
        await self._all_price()

    async def _region(self):
        max_len = 14
        region_len = len(self.__data.get("area_region"))
        if max_len != region_len:
            self.__region_platform = str(', '.join((parameter.get("region") for parameter in self.__data.get("area_region"))))
        else:
            self.__region_platform = self.__Lang.platform.blogger.wholeCountry

    async def _all_price(self):
        self.__price_platform = ""
        for accommodation in self.__data.get("area_accommodation"):
            if accommodation.get("price") is not None:
                self.__price = accommodation.get("price")
                self.__accommodation = accommodation.get("accommodation")
                await self._price()

    async def _price(self):
        text = Template("\n$format - <b>$price</b> $sum")
        text = text.substitute(format=self.__accommodation, price=await func.int_to_str(num=self.__price),
                               sum=self.__Lang.symbol.sum)
        self.__price_platform += text
