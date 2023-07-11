from typing import TypedDict


class AllOrder(TypedDict, total=False):
    allOrder: dict
    orders: dict
    activeOrder: dict
    completedOrder: dict
    area_id: int
    channels: list
    current_channel: int
    order_id: int


class PostModel(TypedDict, total=False):
    blogger_area_id: int
    post_url: str
    area_id: int
    rate: int



