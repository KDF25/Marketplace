import datetime
import json
from math import ceil

from aiogram import types
from natsort import natsorted

from datetime_now import dt_now
from model.form_order import ChannelsModel, FormOrderFinish, DateModel, TimeModel
from model.personal_data import PersonalDataModel
from model.platform import Platform, Values
from text.language.main import Text_main

Txt = Text_main()


class MessageEntityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, types.MessageEntity):
            return {
                "type": obj.type,
                "offset": obj.offset,
                "length": obj.length,
                "url": obj.url,
                "user": obj.user.to_python() if obj.user else None,
                "language": obj.language,
            }
        return json.JSONEncoder.default(self, obj)


class TextFunc:
    @staticmethod
    async def int_to_str(num: int):
        new_num = ""
        num = str(num)
        num_len = len(num)
        for i in range(0, num_len, 3):
            if i < num_len - 3:
                part = num[num_len - 3 - i:num_len - i:]
                new_num = f"{part} {new_num}"
        new_num_len = len(new_num.replace(" ", ""))
        if new_num_len < num_len:
            new_num = f"{num[0:num_len - new_num_len]} {new_num}"
        return new_num.strip()

    @staticmethod
    async def calendar(date: str, turn: str):
        # date = datetime.datetime.strptime(date, "%d.%m.%Y")
        # year = date.year
        # month = date.month
        # if date.month == 1 and turn == "prev":
        #     month = 12
        #     year = date.year - 1
        # elif date.month == 12 and turn == "next":
        #     month = 1
        #     year = date.year + 1
        # elif turn == "prev":
        #     month -= 1
        # elif turn == "next":
        #     month += 1
        # date = datetime.datetime.strftime(datetime.datetime(year=year, month=month, day=date.day), "%d.%m.%Y")
        value = 1
        if turn == "prev":
            value = -1
        elif turn == "next":
            value = 1
        date = datetime.datetime.strftime(datetime.datetime.strptime(date, "%d.%m.%Y") + datetime.timedelta(30) * value, "%d.%m.%Y")
        return date

    async def time(self):
        time = dt_now.now().hour // 3 + 1
        time = 0 if time * 3 >= 24 else time * 3
        time = [f"{time}:00 - {time + 3}:00"]
        return time

    @staticmethod
    async def time_change(time: str, times: list):
        if time in times and len(times) > 1:
            times.remove(time)
        elif time not in times:
            times.append(time)
            times = natsorted(times)
        return times

    @staticmethod
    async def commission(price: int):
        nds = Txt.commission.nds
        bot = Txt.commission.bot
        cost = ceil(price * (1 + bot/100))
        return cost

    @staticmethod
    async def join(parameters: list):
        if len(parameters) == 0:
            return "..."
        else:
            return str(', '.join((parameter for parameter in parameters)))

    # @staticmethod
    async def add_platform(self, data: dict):
        json = Platform(client_id=data.get("client_id"),
                        type=data.get("platform_id"), url=data.get("url"),
                        name=data.get("name"),
                        category=data.get("category").get('id'),
                        description=data.get("description"),
                        sex_ratio=data.get("sex"),
                        text_limit=data.get("symbol"),
                        area_language=await self._list(parameters=data.get("platformLang").get("id"), key="language"),
                        area_region=await self._list(parameters=data.get("regions").get("id"), key="region"),
                        area_age=await self._list(parameters=data.get("age").get("id"), key="age"),
                        area_accommodation=await self._format(data.get("accommodation")))
        return json

    @staticmethod
    async def _list(parameters: list, key: str):
        return [{key: value_id} for value_id in parameters]

    @staticmethod
    async def _format(accommodation: dict):
        list_accommodations = []
        for item in accommodation:
            if item.get("price") is not None:
                list_accommodations.append({"accommodation": item.get("id"), "price": int(item.get("price"))})
        return list_accommodations

    @staticmethod
    async def max_page(units: list):
        on_list = 10
        max_page = ceil(len(units) / on_list)
        return max_page

    @staticmethod
    async def add_entity(data: dict):
        Json = PersonalDataModel(type_legal="entity",
                                 name=str(data.get("title")),
                                 legal_address=str(data.get("legalAddress")),
                                 INN=str(data.get("inn")),
                                 payment_account=str(data.get("paymentAccount")),
                                 bank=str(data.get("bank")),
                                 MFO=str(data.get("mfo")),
                                 phone=str(data.get("phone")))
        return Json

    @staticmethod
    async def add_individual(data: dict):
        Json = PersonalDataModel(type_legal="individual",
                                 name=str(data.get("title")),
                                 legal_address=str(data.get("legalAddress")),
                                 PNFL=str(data.get("pinfl")),
                                 payment_account=str(data.get("paymentAccount")),
                                 bank=str(data.get("bank")),
                                 MFO=str(data.get("mfo")),
                                 phone=str(data.get("phone")))
        return Json

    @staticmethod
    async def add_self_employed_card(data: dict):
        Json = PersonalDataModel(type_legal="self_employed_transit",
                                 name=str(data.get("fio")),
                                 number_registration=data.get("number"),
                                 date_registration=data.get("date"),
                                 PNFL=str(data.get("pinfl")),
                                 transit_account=str(data.get("paymentAccount")),
                                 bank=str(data.get("bank")),
                                 MFO=str(data.get("mfo")),
                                 phone=str(data.get("phone")),
                                 card_number=str(data.get('cardNumber')),
                                 card_date=str(data.get('cardDate')))
        return Json

    @staticmethod
    async def add_self_employed_account(data: dict):
        Json = PersonalDataModel(type_legal="self_employed",
                                 name=str(data.get("fio")),
                                 number_registration=data.get("number"),
                                 date_registration=data.get("date"),
                                 PNFL=str(data.get("pinfl")),
                                 payment_account=str(data.get("paymentAccount")),
                                 bank=str(data.get("bank")),
                                 MFO=str(data.get("mfo")),
                                 phone=str(data.get("phone")))
        return Json

    @staticmethod
    async def get_all_platform(json: dict):
        data = []
        for area in json:
            platform = {}
            platform["id"] = area["id"]
            platform["name"] = area["name"]
            platform["url"] = area["url"]
            platform["subscribers"] = area["subscribers"]
            platform["platformLang"] = {}
            for i in area["area_language"]:
                platform["platformLang"][i["id"]] = i["language"][:2]
            data.append(platform)
        return data

    async def get_platform(self, json: dict):
        data = {}
        lang_id, languages = await self._unpack_values(parameters=json["area_language"], name="language")
        region_id, regions = await self._unpack_values(parameters=json["area_region"], name="region")
        age_id, ages = await self._unpack_values(parameters=json["area_age"], name="age")
        accommodation = [{"id": accommodation["id"], "name": accommodation["accommodation"],
                          "price": accommodation["price"]} for accommodation in json['area_accommodation']]
        data["id"] = json["id"]
        data["name"] = json["name"]
        data["url"] = json["url"]
        data["description"] = json["description"]
        data["platform"] = json["type"]["type"]
        data["platform_id"] = json["type"]["id"]
        data["sex"] = json["sex_ratio"]["id"]
        data["sex_value"] = json["sex_ratio"]["ratio"]
        data["category"] = {"value": json["category"]}
        data["regions"] = Values(id=region_id, values=regions)
        data["age"] = Values(id=age_id, values=ages)
        data["accommodation"] = accommodation
        data["subscribers"] = json["subscribers"]
        data["platformLang"] = Values(id=lang_id, values=languages)
        return data
    
    @staticmethod
    async def _unpack_values(parameters: list, name: str):
        id = []
        values = []
        for parameter in parameters:
            id.append(parameter["id"])
            values.append(parameter[name])
        return id, values

    @staticmethod
    async def _price(parameters: list):
        price = {}
        for parameter in parameters:
            price[parameter["id"]] = parameter["price"]
        return price

    @staticmethod
    async def get_entity(json: dict):
        data = {}
        data["title"] = json.get("name")
        data["legalAddress"] = json.get("legal_address")
        data["inn"] = json.get("INN")
        data["bank"] = json.get("bank")
        data["paymentAccount"] = json.get("payment_account")
        data["phone"] = json.get("phone")
        data["mfo"] = json.get("MFO")
        return data

    @staticmethod
    async def get_individual(json: dict):
        data = {}
        data["title"] = json.get("name")
        data["legalAddress"] = json.get("legal_address")
        data["pinfl"] = json.get("PNFL")
        data["bank"] = json.get("bank")
        data["paymentAccount"] = json.get("payment_account")
        data["phone"] = json.get("phone")
        data["mfo"] = json.get("MFO")
        return data

    @staticmethod
    async def get_self_employed_card(json: dict):
        data = {}
        data["fio"] = json.get("name")
        data["number"] = json.get("number_registration")
        data["date"] = json.get("date_registration")
        data["pinfl"] = json.get("PNFL")
        data["paymentAccount"] = json.get("transit_account")
        data["phone"] = json.get("phone")
        data["bank"] = json.get("bank")
        data["mfo"] = json.get("MFO")
        data["cardNumber"] = json.get("card_number")
        data["cardDate"] = json.get("card_date")
        return data

    @staticmethod
    async def get_self_employed_account(json: dict):
        data = {}
        data["fio"] = json.get("name")
        data["number"] = json.get("number_registration")
        data["date"] = json.get("date_registration")
        data["pinfl"] = json.get("PNFL")
        data["paymentAccount"] = json.get("payment_account")
        data["phone"] = json.get("phone")
        data["bank"] = json.get("bank")
        data["mfo"] = json.get("MFO")
        return data

    @staticmethod
    async def _unpack_time(TIME: list):
        LIST = []
        TIME = natsorted(TIME)
        for i in range(0, len(TIME)):
            x = TIME[i].split(" - ")
            LIST.append(x[0])
            LIST.append(x[1])
        return LIST

    async def sort_time(self, time: list, i=0):
        LIST = []
        time = await self._unpack_time(TIME=time)
        while True:
            try:
                if time[i] == time[i + 1]:
                    time.pop(i + 1)
                    time.pop(i)
                    i = i - 2
                else:
                    i += 1
            except IndexError:
                break
        for i in range(0, len(time), 2):
            LIST.append(f"{time[i]} - {time[i + 1]}")
        LIST = f"{str(', '.join((str(i) for i in LIST)))}"
        return LIST

    @staticmethod
    async def form_order(data: dict):
        channel_list = []
        for channel in data.get("formOrder").get("basket").get("channels"):
            date = datetime.datetime.strptime(channel.get("date"), "%d.%m.%Y")
            time_list = []
            for time in channel.get("time"):
                times = time.split(" - ")
                time_from = times[0]
                time_until = times[-1] if times[-1] != "24:00" else "23:59"
                time_list.append(TimeModel(time_from=time_from, time_until=time_until))
            Json = ChannelsModel(area_id=channel.get("id"),
                                 date=DateModel(year=date.year, month=date.month, day=date.day, time_periods=time_list))
            channel_list.append(Json)
        Json = FormOrderFinish(order_id=data.get("formOrder").get("campaign").get("order_id"), channels=channel_list)
        return Json

    @staticmethod
    async def add_basket(data: dict):
        channel_list = []
        for channel in data.get("formOrder").get("basket").get("channels"):
            Json = ChannelsModel(area_id=channel.get("id"), accommodation=channel.get("current_accommodation")[0])
            channel_list.append(Json)
        Json = {"basket": channel_list}
        return Json

    @staticmethod
    async def repack_time(data: list):
        time_list = []
        for time in data:
            start = time.get("time_from")[:-3]
            finish = time.get("time_until")[:-3]
            time_str = start + " - " + finish
            time_list.append(time_str)
        return time_list



