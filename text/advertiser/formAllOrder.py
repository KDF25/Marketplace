from string import Template

from aiogram.utils.markdown import hlink

from text.fuction.function import TextFunc
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
func = TextFunc()


class FormAllOrderAdvertiser:

    def __init__(self, language: str, data: dict = None):
        self.__data = data
        self.__Lang: Model = Txt.language[language]

    async def menu_all_orders(self):
        text = Template("<b>$active:</b> $active_num\n"
                        "<b>$completed:</b> $completed_num\n\n"
                        "$choose")
        text = text.substitute(active=self.__Lang.allOrder.active, active_num=self.__data.get("active"),
                               completed=self.__Lang.allOrder.completed, completed_num=self.__data.get("completed"),
                               choose=self.__Lang.allOrder.choose)
        return text

    async def menu_active_project(self):
        await self._unpack_campaign()
        text = Template("<b>$campaign_name</b>\n\n"
                        "$all_platform"
                        "$subscribers — $all_subscribers\n"
                        "$coverage — $all_coverage\n\n"
                        "$commission\n"
                        "<b>$cost — $all_cost $sum</b>")
        text = text.substitute(campaign_name=self.__campaign_name, all_platform=self.__all_platform,
                               subscribers=self.__Lang.formOrder.basket.subscribers,
                               all_subscribers=self.__all_subscribers,
                               coverage=self.__Lang.formOrder.basket.coverage, all_coverage=self.__coverage,
                               commission=self.__Lang.formOrder.basket.commission, nds=self.__Lang.formOrder.basket.nds,
                               cost=self.__Lang.formOrder.basket.cost, sum=self.__Lang.formOrder.form.sum,
                               all_cost=await func.int_to_str(num=self.__cost))

        return text

    async def _unpack_campaign(self):
        self.__cost = await func.commission(self.__data.get("amount"))
        self.__campaign_name = self.__data.get("order_name")
        self.__coverage = await func.int_to_str(num=self.__data.get("coverage"))
        self.__all_subscribers = await  func.int_to_str(num=self.__data.get("members"))
        self.__all_platform = ""
        for platform in self.__data.get("purchased"):
            await self._unpack_current_platform(data=platform)
            await self._platform()

    async def _unpack_current_platform(self, data: dict):
        self.__title = data.get("name")
        self.__url = data.get("url")
        self.__rate = "-"
        # self.__subs = round(data.get("subscribers") / 1000)
        # self.__subscribes = await func.int_to_str(num=self.__subs)
        self.__subscribes =  round(data.get("subscribers") / 1000, 1)
        self.__views = round(data.get("views", 0)/ 1000, 1)
        self.__price = await func.int_to_str(num=data.get("price"))
        self.__date = data.get('date')
        time = await func.repack_time(data.get("time_period"))
        self.__time = await func.sort_time(time)
        self.__accommodation = data.get("accommodation")

    async def _platform(self):
        text = Template("$title\n"
                        "⭐$rate | <b>👥$subscribes</b>k | 👀 <b>$views</b>k\n"
                        "🗓$date , ⏰$time\n"
                        "$accommodation - $price $sum\n\n")
        text = text.substitute(title=hlink(url=self.__url, title=self.__title), rate=self.__rate,
                               subscribes=self.__subscribes, views=self.__views,
                               date=self.__date, time=self.__time, accommodation=self.__accommodation,
                               price=self.__price, sum=self.__Lang.formOrder.form.sum)
        self.__all_platform += text

    async def menu_completed_project(self):
        await self._unpack_campaign()
        text = Template("<b>$campaign_name</b>\n\n"
                        "$status\n\n"
                        "$all_platform"
                        "$subscribers — $all_subscribers\n"
                        "$coverage — $all_coverage\n\n"
                        "$commission\n"
                        "<b>$cost — $all_cost $sum</b>")
        text = text.substitute(campaign_name=self.__campaign_name, all_platform=self.__all_platform,
                               status=self.__Lang.formOrder.basket.status,
                               subscribers=self.__Lang.formOrder.basket.subscribers,
                               all_subscribers=self.__all_subscribers,
                               coverage=self.__Lang.formOrder.basket.coverage, all_coverage=self.__coverage,
                               commission=self.__Lang.formOrder.basket.commission, nds=self.__Lang.formOrder.basket.nds,
                               cost=self.__Lang.formOrder.basket.cost, sum=self.__Lang.formOrder.form.sum,
                               all_cost=await func.int_to_str(num=self.__cost))

        return text
