from typing import TypedDict


class Basket(TypedDict, total=False):
    order_id: int
    language: str

