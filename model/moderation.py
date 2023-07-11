from typing import TypedDict


class ModerationModel(TypedDict, total=False):
    area_id: int
    reason: str
