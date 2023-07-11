from typing import TypedDict, Union


class FormOrderModel(TypedDict, total=False):
    selected: list
    basket: dict
    siteRequest: dict
    category: dict
    sex: dict
    regions: dict
    platformLang: dict
    age: dict
    network: dict
    platformTypes: dict


class ChannelListModel(TypedDict, total=False):
    platformList: list
    count: int
    page: int
    pages: int


class PlatformList(TypedDict, total=False):
    offset: int
    limit: int
    language: str
    channel: dict
    other: dict
    word: Union[str, int]


class ChannelModel(TypedDict, total=False):
    category: list
    sex_ratio: int
    age: list
    language: list
    region: list


class OtherModel(TypedDict, total=False):
    type_channel: int
    accommodation: int
    sorted_by: str
    selected: list
    offset: int
    limit: int


class PostModel(TypedDict, total=False):
    name: str
    file_id: str
    text: str
    buttons: str
    comment: str
    type_file: str
    order_id: int


class PlatformTypeModel(TypedDict, total=False):
    types_platform: list
    accommodations: list


class TimeModel(TypedDict, total=False):
    time_from: str
    time_until: str


class DateModel(TypedDict, total=False):
    year: int
    month: int
    day: int
    time_periods: list


class ChannelsModel(TypedDict, total=False):
    area_id: int
    accommodation: int
    price: int
    date: DateModel


class FormOrderFinish(TypedDict, total=False):
    order_id: int
    channels: list







