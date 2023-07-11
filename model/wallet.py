from typing import TypedDict


class WalletModel(TypedDict, total=False):
    type_legal: str
    amount: int
    journal_id: int
    reason: str
