from typing import TypedDict, Union


class CalendarModel(TypedDict, total=False):
    year: int
    month: int
    day: int
    area_id: int



