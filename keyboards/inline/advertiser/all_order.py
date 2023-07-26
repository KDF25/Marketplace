from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class InlineAllOrderAdvertiser():

    def __init__(self, language: str, all_orders: dict = None, orders: dict = None, order_id: int = None,
                 channels: list = None, siteRequest: dict = None):
        self.__markup = None
        self.__language = language
        self.__Lang: Model = Txt.language[language]
        self.__all_orders = all_orders
        self.__orders = orders
        self.__order_id = order_id
        self.__channels = channels
        self.__siteRequest = siteRequest
        self.__back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_all_orders(self):
        markup = InlineKeyboardMarkup(row_width=1)
        active = "active" if self.__all_orders.get('active') != 0 else "zeroCount"
        completed = "completed" if self.__all_orders.get('completed') != 0 else "zeroCount"
        b1 = InlineKeyboardButton(text=f"{self.__Lang.allOrder.active} ({self.__all_orders.get('active')})",
                                  callback_data=active)
        b2 = InlineKeyboardButton(text=f"{self.__Lang.allOrder.completed} ({self.__all_orders.get('completed')})",
                                  callback_data=completed)
        markup.add(b1, b2)
        return markup

    async def menu_orders(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._pages()
        await self._orders()
        self.__markup.add(self.__back)
        return self.__markup

    async def _orders(self):
        for order in self.__orders:
            text = f"{order.get('date')[0:5]} | {order.get('name')}"
            b = InlineKeyboardButton(text=text, callback_data=f"order_{order.get('order_id')}")
            self.__markup.add(b)

    async def _pages(self):
        prev = InlineKeyboardButton(text=self.__Lang.buttons.common.prev, callback_data="prev")
        next = InlineKeyboardButton(text=self.__Lang.buttons.common.next, callback_data="next")
        page = InlineKeyboardButton(text=f"{self.__siteRequest.get('page')} / {self.__siteRequest.get('pages')}", callback_data="void")
        self.__markup.row(prev, page, next)

    async def menu_active_project(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.task, callback_data=f"CheckPost_{self.__order_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.blogger, callback_data=f"SendBlogger")
        markup.add(b1, b2, self.__back)
        return markup

    async def menu_completed_project(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.task, callback_data=f"CheckPost_{self.__order_id}")
        markup.add(b1, self.__back)
        return markup

    async def menu_send_blogger(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._send_blogger()
        b = InlineKeyboardButton(text=self.__Lang.buttons.post.blogger, callback_data="SendBloggerAccept")
        self.__markup.add(b, self.__back)
        return self.__markup

    async def _send_blogger(self):
        for order in self.__orders.get("purchased"):
            text = await self._append_parameter(parameter=order.get('area_id'), parameters=self.__channels, value=order.get('name'))
            b = InlineKeyboardButton(text=text, callback_data=f"channel_{order.get('area_id')}")
            self.__markup.add(b)

    @staticmethod
    async def _append_parameter(parameter, parameters, value):
        if parameter in parameters:
            return "✅ " + value
        else:
            return value


