from typing import TypedDict


class User(TypedDict, total=False):
    lang: str
    email: str
    username: str
    password: str
    password_hash: str
    role: str
    wallet: int
    code: int
    token: dict


class Code(TypedDict, total=False):
    email: str
    password: str
    code: int


class Token(TypedDict, total=False):
    token: str



