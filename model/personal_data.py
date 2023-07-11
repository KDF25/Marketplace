from typing import TypedDict, Union


class PersonalDataModel(TypedDict, total=False):
    type_legal: str
    name: str
    legal_address: str
    INN: str
    PNFL: str
    bank: str
    MFO: str
    phone: str
    number_registration: int
    date_registration: str
    payment_account: str
    transit_account: str
    card_number: str
    card_date: str

