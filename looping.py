from database.postgresql import Database
from database.fastapi import FastApi
import asyncio

loop = asyncio.get_event_loop()
pg = Database(loop=loop)
fastapi = FastApi(loop=loop)
