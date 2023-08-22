import calendar
import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from looping import fastapi
from model.platform import Params
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class InlinePlatformBlogger():

    def __init__(self, language: str,
                 platform: dict = None,
                 category: dict = None,
                 page: int = None,
                 platform_lang: dict = None,
                 regions: dict = None,
                 age: dict = None,
                 formats: dict = None,
                 token: dict = None,
                 date: str = None,
                 calendar_list: list = None,
                 siteRequest: dict = None,
                 channel_type: str = None):
        self.__markup = None
        self.__category = category
        self.__platform = platform
        self.__page = page
        self.__platform_lang = platform_lang
        self.__regions = regions
        self.__formats = formats
        self.__language = language
        self.__age = age
        self.__token = token
        self.__siteRequest = siteRequest
        self.__channel_type = channel_type
        self.__date = datetime.datetime.strptime(date, "%d.%m.%Y") if date is not None else None
        self.__calendar_list = calendar_list
        self.__Lang: Model = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")
        self.__confirm = InlineKeyboardButton(text=self.__Lang.buttons.common.confirm, callback_data="confirm")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_add(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.add, callback_data="add")
        markup.add(b1)
        return markup

    async def menu_delete(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.delete, callback_data="deleteAnyway")
        markup.add(b1, self.__back)
        return markup

    async def menu_all_platform(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._pages_platform()
        await self._all_platform()
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.add, callback_data="add")
        self.__markup.add(b1)
        return self.__markup

    async def _pages_platform(self):
        prev = InlineKeyboardButton(text=self.__Lang.buttons.common.prev, callback_data="prev")
        next = InlineKeyboardButton(text=self.__Lang.buttons.common.next, callback_data="next")
        page = InlineKeyboardButton(text=f"{self.__siteRequest.get('page')} / {self.__siteRequest.get('pages')}", callback_data="void")
        self.__markup.row(prev, page, next)

    async def _all_platform(self):
        for platform in self.__platform:
            b = InlineKeyboardButton(text=f"✍️{platform['name']}", callback_data=f"platform_{platform['id']}")
            self.__markup.add(b)

    async def menu_telegram(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.check, callback_data="check")
        markup.add(b1, self.__back)
        return markup

    async def menu_other(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.authorization, callback_data="authorization")
        markup.add(b1, self.__back)
        return markup

    async def menu_preview(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.main.change, callback_data="change")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.platform.main.calendar, callback_data="calendar")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.platform.main.delete, callback_data="delete")
        markup.add(b1, b2, b3, self.__back)
        return markup

    async def menu_change(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.change.description, callback_data="description")
        markup.add(b1)
        if self.__channel_type == "telegram":
            b2 = InlineKeyboardButton(text=self.__Lang.buttons.platform.change.url, callback_data="url")
            markup.add(b2)
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.platform.change.parameters, callback_data="parameters")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.platform.change.price, callback_data="price")
        markup.add(b3, b4, self.__back)
        return markup

    async def menu_parameters(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.parameters.sex, callback_data="Sex")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.platform.parameters.age, callback_data="Age")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.platform.parameters.lang, callback_data="Lang")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.platform.parameters.region, callback_data="Region")
        markup.add(b1, b2, b3, b4, self.__back)
        return markup

    async def menu_kind(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._kind()
        self.__markup.add(self.__back)
        return self.__markup

    async def _kind(self):
        params = Params(language=self.__language, offset=0, limit=40)
        all_kind = await fastapi.get_channel_types(params=params, token=self.__token)
        for kind in all_kind.get("types"):
            b = InlineKeyboardButton(text=kind.get("name").title(), callback_data=f"kind_{kind.get('id')}")
            self.__markup.insert(b)

    async def menu_authorization(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.authorization, callback_data="authorization")
        markup.add(b1, self.__back)
        return markup

    async def menu_platform(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.sex, callback_data="sex")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.age, callback_data="age")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.lang, callback_data="lang")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.region, callback_data="region")
        markup.add(b1, b2, b3, b4, self.__back)
        return markup

    async def _append(self, parameter: [str, int], parameters: list, value: str):
        if parameter in parameters:
            return "✅ " + value
        else:
            return value

    async def menu_lang(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._buttons(parameters=self.__platform_lang, callback="platformLang")
        self.__markup.add(self.__confirm, self.__back)
        return self.__markup

    async def menu_age(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._buttons(parameters=self.__age, callback="age")
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def _age(self):
        params = Params(language=self.__language, offset=0, limit=40)
        all_age = await fastapi.get_channel_age_ratios(params=params, token=self.__token)
        for index, sex in enumerate(all_age.get("types")):
            b = InlineKeyboardButton(text=sex.get("name"), callback_data=f"age_{sex.get('id')}")
            self.__markup.insert(b)

    async def menu_sex(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._sex()
        self.__markup.add(self.__back)
        return self.__markup

    async def _sex(self):
        params = Params(language=self.__language, offset=0, limit=40)
        all_sex = await fastapi.get_channel_sex_ratios(params=params, token=self.__token)
        for index, sex in enumerate(all_sex.get("types")):
            b = InlineKeyboardButton(text=sex.get("name"), callback_data=f"sex_{sex.get('id')}")
            if index % 3 == 0:
                self.__markup.add(b)
            else:
                self.__markup.insert(b)

    async def menu_format(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        # await self._buttons(parameters=self.__formats, callback="format")
        await self._format()
        clean = InlineKeyboardButton(text=self.__Lang.buttons.common.clean, callback_data="clean")
        self.__markup.add(clean, self.__confirm, self.__back)
        return self.__markup

    async def _format(self):
        for accommodation in self.__formats:
            text = accommodation.get('name')
            text = text if accommodation.get('price') is None else "✅ " + text
            b = InlineKeyboardButton(text=text, callback_data=f"format_{accommodation.get('id')}")
            self.__markup.insert(b)

    async def menu_check(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.alright, callback_data="alright")
        markup.add(b1, self.__back)
        return markup

    async def menu_category(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._category()
        prev = InlineKeyboardButton(text=self.__Lang.buttons.common.prev, callback_data="prev")
        next = InlineKeyboardButton(text=self.__Lang.buttons.common.next, callback_data="next")
        page = InlineKeyboardButton(text=f"{self.__page} / {self.__category.get('max_page')}", callback_data="void")
        self.__markup.row(prev, page, next)
        self.__markup.add(self.__back)
        return self.__markup

    async def _category(self):
        on_list = 10
        start = on_list * (self.__page - 1)
        stop = on_list * self.__page
        for category in self.__category.get('all_values')[start: stop]:
            b = InlineKeyboardButton(text=category.get("name"), callback_data=f"category_{category.get('id')}")
            self.__markup.insert(b)

    async def menu_region(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._buttons(parameters=self.__regions, callback="region")
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def _buttons(self, parameters: dict, callback: str):
        for parameter in parameters.get("all_values"):
            text = await self._append(parameter=parameter.get('id'), value=parameter.get("name"),
                                      parameters=parameters.get("id"))
            b = InlineKeyboardButton(text=text, callback_data=f"{callback}_{parameter.get('id')}")
            self.__markup.insert(b)

    async def menu_calendar(self):
        self.__markup = InlineKeyboardMarkup(row_width=7)
        await self._calendar_listing()
        await self._calendar()
        self.__markup.add(self.__back)
        return self.__markup

    async def _calendar_listing(self):
        prev = InlineKeyboardButton(text=self.__Lang.buttons.common.prev, callback_data="prev")
        next = InlineKeyboardButton(text=self.__Lang.buttons.common.next, callback_data="next")
        text = datetime.datetime.strftime(self.__date, '%B')
        mounth = InlineKeyboardButton(text=text, callback_data="void")
        self.__markup.add(prev, mounth, next)

    async def _calendar(self):
        year = self.__date.year
        month = self.__date.month
        days = calendar.Calendar(calendar.MONDAY).monthdayscalendar(year=year, month=month)
        for week in days:
            for i, day in enumerate(week):
                if day != 0:
                    date = datetime.datetime(year=year, month=month, day=day)
                    date = datetime.datetime.strftime(date, "%d.%m.%Y")
                    if date in self.__calendar_list:
                        text = f"🔒{day}"
                    else:
                        text = day
                    callback = f"day_{date}"
                else:
                    callback = "void"
                    text = "▫"
                b = InlineKeyboardButton(text=text, callback_data=callback)
                if i == 0:
                    self.__markup.add(b)
                else:
                    self.__markup.insert(b)






