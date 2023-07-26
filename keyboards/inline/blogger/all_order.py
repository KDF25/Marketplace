from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class InlineAllOrderBlogger():

    def __init__(self, language: str, all_channels: list = None, channel: dict = None, orders: dict = None,
                 current_id: int = None, siteRequest: dict = None):
        self.__markup = None
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__all_channels = all_channels
        self.__channel = channel
        self.__current_id = current_id
        self.__orders = orders
        self.__siteRequest = siteRequest
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_all_orders(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._pages()
        await self._all_orders()
        return self.__markup

    async def _all_orders(self):
        for channel in self.__all_channels:
            wait = channel.get("wait")
            active = channel.get("active")
            completed = channel.get("completed")
            count = wait + active + completed
            text = f"{channel.get('name')} ({count})"
            callback = f"platform_{channel.get('area_id')}" if count != 0 else "zeroCount"
            b = InlineKeyboardButton(text=text, callback_data=callback)
            self.__markup.add(b)

    async def _pages(self):
        prev = InlineKeyboardButton(text=self.__Lang.buttons.common.prev, callback_data="prev")
        next = InlineKeyboardButton(text=self.__Lang.buttons.common.next, callback_data="next")
        page = InlineKeyboardButton(text=f"{self.__siteRequest.get('page')} / {self.__siteRequest.get('pages')}", callback_data="void")
        self.__markup.row(prev, page, next)

    async def menu_platform(self):
        markup = InlineKeyboardMarkup(row_width=1)
        wait = "expects" if self.__channel.get('wait') != 0 else "zeroCount"
        active = "active" if self.__channel.get('active') != 0 else "zeroCount"
        completed = "completed" if self.__channel.get('completed') != 0 else "zeroCount"
        b1 = InlineKeyboardButton(text=f"{self.__Lang.allOrder.expects} ({self.__channel.get('wait')})",
                                  callback_data=wait)
        b2 = InlineKeyboardButton(text=f"{self.__Lang.allOrder.active} ({self.__channel.get('active')})",
                                  callback_data=active)
        b3 = InlineKeyboardButton(text=f"{self.__Lang.allOrder.completed} ({self.__channel.get('completed')})",
                                  callback_data=completed)
        markup.add(b1, b2, b3, self.__back)
        return markup

    async def menu_orders(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._pages()
        await self._orders()
        self.__markup.add(self.__back)
        return self.__markup

    async def _orders(self):
        for order in self.__orders:
            if order.get("area_id") == self.__current_id:
                text = f"{order.get('date')[0:5]} | {order.get('name')}"
                b = InlineKeyboardButton(text=text, callback_data=f"order_{order.get('id')}")
                self.__markup.add(b)

