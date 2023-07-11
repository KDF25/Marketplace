import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from looping import fastapi
from model.platform import Params
from text.language.main import Text_main
import calendar


Txt = Text_main()


class InlineFormOrderAdvertiser():

    def __init__(self, language: str,
                 platform: dict = None,
                 category: dict = None,
                 page: int = None,
                 network: dict = None,
                 platform_lang: dict = None,
                 all_channels: dict = None,
                 platform_list: list = None,
                 platform_types: dict = None,
                 accommodation_filter: str = None,
                 accommodation: dict = None,
                 main_filter: str = None,
                 search: str = None,
                 regions: dict = None,
                 age: dict = None,
                 formats: dict = None,
                 token: dict = None,
                 url_buttons: list = None,
                 media_button: bool = None,
                 comment_button: bool = None,
                 calendar_list: list = None,
                 date: str = None,
                 time: list = None,
                 status_category=None,
                 status_parameters=None,
                 status_network=None,
                 status_sex=None,
                 status_age=None,
                 status_lang=None,
                 status_region=None):
        self.__markup = None
        self.__category = category
        self.__platform = platform
        self.__page = page
        self.__network = network
        self.__platform_lang = platform_lang
        self.__all_channels = all_channels
        self.__platform_list = platform_list
        self.__platform_types = platform_types
        self.__accommodation_filter = accommodation_filter
        self.__accommodation = accommodation
        self.__main_filter = main_filter
        self.__regions = regions
        self.__formats = formats
        self.__language = language
        self.__age = age
        self.__token = token
        self.__search = search
        self.__url_buttons = url_buttons
        self.__media_button = media_button
        self.__comment_button = comment_button
        self.__calendar_list = calendar_list
        self.__time = time
        self.__date = datetime.datetime.strptime(date, "%d.%m.%Y") if date is not None else None
        self.__Lang = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")
        self.__confirm = InlineKeyboardButton(text=self.__Lang.buttons.common.confirm, callback_data="confirm")
        self.__clean = InlineKeyboardButton(text=self.__Lang.buttons.common.clean, callback_data="clean")
        self.__status_category = True if status_category is not None and status_category != 0 else False
        self.__status_parameters = True if status_parameters is not None and status_parameters != 0 else False
        self.__status_network = True if status_network is not None and status_network != 0 else False
        self.__status_sex = True if status_sex is not None and status_sex != 0 else False
        self.__status_age = True if status_age is not None and status_age != 0 else False
        self.__status_lang = True if status_lang is not None and status_lang != 0 else False
        self.__status_region = True if status_region is not None and status_region != 0 else False

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_back_web_app(self, token: str, user_id: int):
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardMarkup(text=self.__Lang.buttons.common.back,
                                    web_app=WebAppInfo(url=f'https://laappetit.uz?token={token}&user_id={user_id}'))
        markup.add(back)
        return markup

    async def menu_form_order(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_category,
                                                                    value=self.__Lang.buttons.formOrder.category),
                                  callback_data="Category")
        b2 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_parameters,
                                                                    value=self.__Lang.buttons.formOrder.parameters),
                                  callback_data="parameters")
        b3 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_network,
                                                                    value=self.__Lang.buttons.formOrder.network),
                                  callback_data="network")
        markup.add(b1, b2, b3, self.__confirm)
        return markup

    async def menu_delete(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.delete, callback_data="deleteAnyway")
        markup.add(b1, self.__back)
        return markup

    async def menu_parameters(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_sex,
                                                                    value=self.__Lang.buttons.platform.parameters.sex),
                                  callback_data="Sex")
        b2 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_age,
                                                                    value=self.__Lang.buttons.platform.parameters.age),
                                  callback_data="Age")
        b3 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_lang,
                                                                    value=self.__Lang.buttons.platform.parameters.lang),
                                  callback_data="Lang")
        b4 = InlineKeyboardButton(text=await self._status_parameter(status=self.__status_region,
                                                                    value=self.__Lang.buttons.platform.parameters.region),
                                  callback_data="Region")
        markup.add(b1, b2, b3, b4).add(self.__confirm).add(self.__back)
        return markup

    async def menu_kind(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._buttons(parameters=self.__network, callback="kind")
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def menu_platform(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.sex, callback_data="sex")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.age, callback_data="age")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.lang, callback_data="lang")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.platform.platform.region, callback_data="region")
        markup.add(b1, b2, b3, b4).add(self.__confirm).add(self.__back)
        return markup

    @staticmethod
    async def _append(parameter: [str, int], parameters: list, value: str):
        if parameter in parameters:
            return "✅ " + value
        else:
            return value

    @staticmethod
    async def _status_parameter(status, value: str):
        if status is True:
            return "✅ " + value
        else:
            return value

    async def menu_lang(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._buttons(parameters=self.__platform_lang, callback="platformLang")
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def menu_age(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._buttons(parameters=self.__age, callback="age")
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

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
        await self._buttons(parameters=self.__formats, callback="format")
        self.__markup.add(self.__clean, self.__confirm, self.__back)
        return self.__markup

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
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def _category(self):
        on_list = 10
        start = on_list * (self.__page - 1)
        stop = on_list * self.__page
        for category in self.__category.get('all_values')[start: stop]:
            text = await self._append(parameter=category.get('id'), value=category.get("name"), parameters=self.__category.get("id"))
            b = InlineKeyboardButton(text=text, callback_data=f"category_{category.get('id')}")
            self.__markup.insert(b)

    async def menu_region(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._buttons(parameters=self.__regions, callback="region")
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def _buttons(self, parameters: dict, callback: str):
        for index, parameter in enumerate(parameters.get("all_values")):
            text = await self._append(parameter=parameter.get('id'), value=parameter.get("name"),
                                      parameters=parameters.get("id"))
            b = InlineKeyboardButton(text=text, callback_data=f"{callback}_{parameter.get('id')}")
            if index == 0:
                self.__markup.add(b)
            else:
                self.__markup.insert(b)

    async def menu_all_platform(self):
        self.__markup = InlineKeyboardMarkup(row_width=4)
        await self._pages_platform()
        await self._main_filter()
        await self._buttons(parameters=self.__platform_types, callback="platformFilter")
        await self._accommodation_filter()
        await self._search_button()
        await self._all_platform()
        self.__markup.add(self.__back)
        return self.__markup

    async def _pages_platform(self):
        prev = InlineKeyboardButton(text=self.__Lang.buttons.common.prev, callback_data="prev")
        next = InlineKeyboardButton(text=self.__Lang.buttons.common.next, callback_data="next")
        page = InlineKeyboardButton(text=f"{self.__all_channels.get('page')} / {self.__all_channels.get('pages')}", callback_data="void")
        self.__markup.row(prev, page, next)

    async def _main_filter(self):
        subs = self.__Lang.buttons.filters.subscribers.asc
        money = self.__Lang.buttons.filters.money.default
        callback_subs = "subs_reverse"
        callback_money = "price_default"
        if self.__main_filter == "subs_default":
            subs = self.__Lang.buttons.filters.subscribers.asc
            money = self.__Lang.buttons.filters.money.default
            callback_subs = "subs_reverse"
            callback_money = "price_default"
        elif self.__main_filter == "subs_reverse":
            subs = self.__Lang.buttons.filters.subscribers.desc
            money = self.__Lang.buttons.filters.money.default
            callback_subs = "subs_default"
            callback_money = "price_default"
        elif self.__main_filter == "price_default":
            subs = self.__Lang.buttons.filters.subscribers.default
            money = self.__Lang.buttons.filters.money.asc
            callback_subs = "subs_default"
            callback_money = "price_reverse"
        elif self.__main_filter == "price_reverse":
            subs = self.__Lang.buttons.filters.subscribers.default
            money = self.__Lang.buttons.filters.money.desc
            callback_subs = "subs_default"
            callback_money = "price_default"
        b1 = InlineKeyboardButton(text=subs, callback_data=callback_subs)
        b2 = InlineKeyboardButton(text=money, callback_data=callback_money)
        self.__markup.add(b1, b2)

    async def _accommodation_filter(self):
        for accommodation in self.__accommodation:
            if accommodation.get('id') == self.__accommodation_filter:
                b = InlineKeyboardButton(text="🔄" + accommodation.get("name"), callback_data=f"accommFilter_{self.__accommodation_filter}")
                self.__markup.add(b)
                break

    async def _search_button(self):
        if self.__search is None:
            search = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.search, callback_data="search")
        else:
            search = InlineKeyboardButton(text=f"❌🔎 «{self.__search}...»", callback_data="deleteSearch")
        self.__markup.add(search)

    async def _all_platform(self):
        for platform in self.__all_channels.get('platformList'):
            name = '🛒' + platform.get('name')
            platform_id = platform.get('id')
            b = InlineKeyboardButton(text=name, callback_data=f"platform_{platform_id}")
            self.__markup.add(b)

    async def menu_current_platform(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._current_accommodation()
        basket = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.addBasket, callback_data="addBasket")
        self.__markup.add(basket).add(self.__back)
        return self.__markup

    async def _current_accommodation(self):
        for accommodation in self.__accommodation['area_accommodation']:
            text = await self._append(parameter=accommodation['id'], value=accommodation['accommodation'],
                                      parameters=self.__accommodation['current_accommodation'])
            b = InlineKeyboardButton(text=text, callback_data=f"accommodation_{accommodation['id']}")
            self.__markup.add(b)

    async def menu_basket(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._basket()
        # back = InlineKeyboardMarkup(text=self.__Lang.buttons.common.back, web_app=WebAppInfo(url=f'https://laappetit.uz?token={token}&user_id={user_id}'))
        # self.__markup.add(back)
        return self.__markup

    async def _basket(self):
        for platform in self.__platform_list:
            name = '❌' + platform.get('name')
            platform_id = platform.get('id')
            b = InlineKeyboardButton(text=name, callback_data=f"delete_{platform_id}")
            self.__markup.add(b)

    async def menu_search_filters(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.find, callback_data="find")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.category, callback_data="Category")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.parameters, callback_data="parameters")
        markup.add(b1, b2, b3, self.__confirm, self.__back)
        return markup

    async def menu_post(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._button_url()
        await self._button_media()
        await self._button_comment()
        self.__markup.add(self.__back)
        return self.__markup

    async def menu_check_post(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        if self.__url_buttons is not None:
            await self._url_buttons()
        return self.__markup

    async def _button_url(self):
        if self.__url_buttons is None:
            b = InlineKeyboardButton(text="➕" + self.__Lang.buttons.formOrder.url, callback_data="url")
        else:
            await self._url_buttons()
            b = InlineKeyboardButton(text="❌" + self.__Lang.buttons.formOrder.url, callback_data="deleteUrl")
        self.__markup.add(b)

    async def _url_buttons(self):
        for buttons in self.__url_buttons:
            for i, button in enumerate(buttons):
                text, url = button.split("-")
                url = url.replace(' ', '')
                b = InlineKeyboardButton(text=text, url=url)
                if i == 0:
                    self.__markup.add(b)
                else:
                    self.__markup.insert(b)

    async def _button_media(self):
        if self.__media_button is False:
            b = InlineKeyboardButton(text="📎" + self.__Lang.buttons.formOrder.media, callback_data="media")
        else:
            b = InlineKeyboardButton(text="❌" + self.__Lang.buttons.formOrder.media, callback_data="deleteMedia")
        self.__markup.add(b)

    async def _button_comment(self):
        if self.__comment_button is False:
            b = InlineKeyboardButton(text="✍" + self.__Lang.buttons.formOrder.comment, callback_data="comment")
        else:
            b = InlineKeyboardButton(text="❌" + self.__Lang.buttons.formOrder.comment, callback_data="deleteComment")
        self.__markup.add(b)

    async def menu_all_dates(self):
        self.__markup = InlineKeyboardMarkup(row_width=7)
        await self._all_dates()
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def _all_dates(self):
        for platform in self.__platform_list:
            name = '🗓' + platform.get('name')
            platform_id = platform.get('id')
            date = "" if platform.get('time') is None else f" ({platform.get('date')})"
            text = name + date
            b = InlineKeyboardButton(text=text, callback_data=f"calendar_{platform_id}")
            self.__markup.add(b)

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
        month = InlineKeyboardButton(text=text, callback_data="void")
        self.__markup.add(prev, month, next)

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
                        callback = "busyDate"
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

    async def menu_time(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        text = self.__Lang.buttons.formOrder.allTime if len(self.__time) != 8 else "✅" + self.__Lang.buttons.formOrder.allTime
        b = InlineKeyboardButton(text=text, callback_data="allTime")
        self.__markup.add(b)
        await self._time()
        self.__markup.add(self.__confirm).add(self.__back)
        return self.__markup

    async def _time(self):
        for i in range(0, 24, 3):
            if i != 21:
                Time = str(f"{i}:00 - {i + 3}:00")
            else:
                Time = str(f"{i}:00 - {i + 2}:59")
            b_time = InlineKeyboardButton(text=await self._append(parameter=Time, parameters=self.__time, value=Time),
                                          callback_data=f"time_{Time}")
            if i == 0:
                self.__markup.add(b_time)
            else:
                self.__markup.insert(b_time)

    async def menu_last_preview(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.order, callback_data="order")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.formOrder.checkPost, callback_data="checkPost")
        markup.add(b1, b2, self.__back)
        return markup



