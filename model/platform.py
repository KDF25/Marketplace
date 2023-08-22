from typing import TypedDict, Union


class Validate(TypedDict, total=False):
    type: int
    url: str
    code: int

class Params(TypedDict, total=False):
    language: str
    category_id: int
    channel_type: int
    offset: int
    limit: int


class GetValue(TypedDict, total=False):
    language: str
    channel_id: int
    category_id: int
    region_id: int
    lang_id: int
    ratio_id: int
    age_id: int
    acc_id: int


class Values(TypedDict, total=False):
    id: list
    page: int
    max_page: int
    values: list
    all_values:  Union[list, dict]


class Platform(TypedDict, total=False):
    client_id: int
    type: int
    url: str
    name: str
    category: int
    description: str
    sex_ratio: int
    text_limit: Union[int, None]
    area_language: list
    area_region: list
    area_age: list
    area_accommodation: list


class GetPlatform(TypedDict, total=False):
    area_id: int
    language: str
    limit: int
    offset: int


class UpdatePlatform(TypedDict, total=False):
    area_id: int
    name: str
    description: int
    url: str
    languages: list
    regions: list
    ages: list
    accommodations: list


class Accommodation(TypedDict, total=False):
    accommodation: int
    price: int

