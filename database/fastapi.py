import asyncio
import time

from aiogram import types
from aiohttp import FormData, ClientSession, ClientResponse, TCPConnector

import config

domain = config.domain
telegram_url = f"https://api.telegram.org/file/bot{config.token}/"




class FastApi:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.__json = None
        # self.pool: asyncio.pool.Pool = loop.run_until_complete(
        #     asyncpg.create_pool(
        #         database="Marketplace",
        #         user=config.PGUSER,
        #         password=config.PASSWORD,
        #         host=config.ip,
        #     ))
        self.pool = True

    async def fastapi_start(self):
        if self.pool:
            print('FastApi connected ok!')

    ##########################################################################################################

    # Authorization
    async def exist_user(self, email: str):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            params = {"email": email}
            response = await session.get(url=f"/api/v1/reg/exist", params=params)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def create_user(self, user: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/reg/user", json=user)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def send_code(self, email: str):
        json = {"email": email}
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/reg/send/email", json=json)
            print(response.status)
            print(await response.json())
            return response.status

    async def check_code(self, code: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/reg/verify/email", json=code)
            print(response.status)
            print(await response.json())
            return response.status

    async def update_password(self, code: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.put(url="/api/v1/reg/update/password", json=code)
            print(response.status)
            print(await response.json())
            return response.status

    ##########################################################################################################




    ##########################################################################################################

    # get token
    async def get_token(self, user: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/reg/oauth", data=user)
            print(response.status)
            print(await response.json())
            # print('\t', await self._token(token=await response.json()))
            return await response.json()

    async def _token(self, token: dict):
        return {"Authorization": f"{token['token_type']} {token['access_token']}"}

    async def get_channel_categories(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/categories", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_category(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/category", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_company_categories(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/company/categories", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_company_category(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/company/category", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_regions(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/regions", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_region(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/region", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_types(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/types", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_type(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/type", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_type_short(self,  token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/type/short")
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_languages(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/languages", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_language(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/language", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_sex_ratios(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/sex/ratios", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_sex_ratio(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/sex/ratio", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_age_ratios(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/ages", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_age_ratio(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/age", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_accommodations(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/accommodations", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_channel_accommodation(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/data/channel/accommodation", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    ##########################################################################################################

    async def validate_url(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/track/validate/url", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def verify_channel(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/track/check/channel", json=json)
            print(response.status)
            print(await response.json())
            return response.status

    ##########################################################################################################

    async def update_language(self, code: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/reg/update/language", json=code)
            print(response.status)
            print(await response.json())
            return response.status

    async def add_platform(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/blogger/area", json=json)
            print(response.status)
            print(await response.json())
            return response.status

    ##########################################################################################################

    async def add_type_legal(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/legal/add", json=json)
            print(await response.json())
            return response.status

    ##########################################################################################################

    async def get_active_legal(self, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/legal/active")
            print(response.status)
            print(await response.json())
            return await response.json()

    async def change_role(self, role: str, token: dict):
        json = {"role": role}
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/roles/", params=json)
            print(response)
            print(response.status)
            print(await response.json())
            return response.status

    ##########################################################################################################

    async def get_areas(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/blogger/areas", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_area(self,  params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/blogger/area", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def delete_area(self, area_id: int, token: dict):
        params = {"area_id": area_id}
        headers = await self._token(token=token)
        print(params)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.delete(url="/api/v1/blogger/area", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_languages(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/languages", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_regions(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/regions", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_ages(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/ages", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_sex(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/sexratio", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_accommodations(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/accommodations", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_name(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/name", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def update_description(self, params: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.put(url="/api/v1/blogger/area/description", json=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    ##########################################################################################################

    async def get_balance(self, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/wallet/balance")
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_history_wallet(self, params:dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/wallet/history", params=params)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def payment_payme(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/wallet/deposit/payme", json=json)
            print("payme", response.status)
            print(await response.json())
            return response.status

    async def payment_click(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/wallet/deposit/click", json=json)
            print(response.status)
            print(await response.json())
            return response.status

    async def payment_didox(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/wallet/deposit/didox", json=json)
            print(response.status)
            print(await response.json())
            return response.status

    async def withdraw(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/wallet/withdrawal/request", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def withdraw_accept(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/wallet/withdrawal/accept", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def withdraw_reject(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/wallet/withdrawal/reject", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def get_on_withdraw(self):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.get(url="/api/v1/moderation/withdrawals/waiting")
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    ##########################################################################################################

    async def moderation(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/moderation/channel/check/telegram", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def moderation_accept(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/moderation/channel/accept/telegram", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def moderation_reject(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/moderation/channel/reject", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def get_on_moderation(self):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.get(url="/api/v1/moderation/channels/waiting")
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def get_platform_for_group(self, params: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.get(url="/api/v1/moderation/search/channel", params=params)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def ban_platform(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/moderation/channel/ban", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def unban_platform(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/moderation/channel/unban", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    ##########################################################################################################

    async def get_platform_list(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/sample", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_search_list(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/search", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    ##########################################################################################################

    async def get_info_month(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/blogger/calendar/month", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def set_status_on_day(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/blogger/calendar/month/day/marker", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    ##########################################################################################################

    async def get_unpaid_basket(self, language: str, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url=f"/api/v1/advertiser/order/unpaid/basket?language={language}")
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def add_unpaid_basket(self, json: dict, token: dict):
        print("add basket ", json)
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/unpaid/basket", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_basket(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url=f"/api/v1/advertiser/order/basket", params=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    ##########################################################################################################

    async def create_order(self, json: dict, token: dict):
        print("create_order", json)
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/create", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def upload_text(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/post/upload/text", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def upload_file(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/post/upload/file", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def upload_buttons(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/post/upload/buttons", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def upload_comment(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/post/upload/comment", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def add_channels(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/advertiser/order/add/channels", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def get_post(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/advertiser/order/post", params=params)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def get_post_moderation(self, params: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.get(url="/api/v1/advertiser/order/moderation/post", params=params)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()


    async def get_list_client_id(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/channels/masters", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    #####################################################################################################

    async def sender(self, token: dict, json: dict):
        headers = await self._token(token=token)
        self.__json = json
        await self._file_type()
        async with ClientSession() as session:
            async with session.get(self.__tg_url) as resp:
                await self._processing_file(response=resp)
                async with session.post(url=f"{domain}{self.__url}?order_id={self.__json.get('order_id')}",
                                        data=self.__data, headers=headers) as response:
                    # print("response", response)
                    # print(await response.json())
                    return response.status

    async def _file_type(self):
        if self.__json.get("type_file") == "photo":
            self.__url = "/api/v1/advertiser/order/post/upload/photo"
            # await self._telegram()
        elif self.__json.get("type_file") == "video":
            self.__url = "/api/v1/advertiser/order/post/upload/video"
            # await self._telegram()
        elif self.__json.get("type_file") == "document":
            self.__url = "/api/v1/advertiser/order/post/upload/file"
        await self._telegram()

    async def _telegram(self):
        Time = int(time.time())
        file1: types.File = await config.bot.get_file(file_id=self.__json.get("file_id"))
        extension = file1.file_path.split(".")[-1].lower()
        self.__tg_url = telegram_url + file1.file_path
        self.__name = f"{Time}{self.__json.get('type_file')}_{self.__json.get('order_id')}.{extension}"

    async def _processing_file(self, response: ClientResponse):
        self.__data = FormData()
        self.__data.add_field("file", value=response.content, filename=self.__name,
                              content_type="application/multipart/form-data")

    #####################################################################################################

    async def all_orders_advertiser(self, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/advertiser/all")
            print(response.status)
            print(await response.json())
            return await response.json()

    async def all_active_advertiser(self, token: dict, params: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/advertiser/active", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def all_completed_advertiser(self, token: dict,  params: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/advertiser/completed", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    #####################################################################################################

    async def all_orders_blogger(self, token: dict, params: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/blogger/all", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def all_wait_blogger(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/blogger/wait", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def all_active_blogger(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/blogger/active", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def all_completed_blogger(self, params: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url="/api/v1/basket/show/blogger/completed", params=params)
            print(response.status)
            print(await response.json())
            return await response.json()

    async def project_blogger(self, blogger_area_id: int, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.get(url=f"/api/v1/basket/show/blogger/order?blogger_area_id={blogger_area_id}")
            print("project_blogger", response.status, "\t",blogger_area_id)
            print(await response.json())
            return response.status, await response.json()

    #####################################################################################################

    async def blogger_accept(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/blogger/order/accept", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def blogger_reject(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/blogger/order/reject", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def blogger_check_post(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/blogger/order/check", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def advertiser_accept(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/advertiser/post/accept", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def advertiser_reject(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/advertiser/post/reject", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def favor_blogger(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/basket/show/moderation/post/accept", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def favor_advertiser(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/basket/show/moderation/post/reject", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def statistics(self, json: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.post(url="/api/v1/statistics/", json=json)
            print(response.status)
            print(await response.json())
            return await response.json()

    #####################################################################################################

    async def rate_post(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/blogger/area/rate/", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def send_post(self, json: dict, token: dict):
        headers = await self._token(token=token)
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector, headers=headers) as session:
            response = await session.post(url="/api/v1/basket/show/blogger/order/check/opportunity", json=json)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def moderation_post(self, blogger_area_id: int):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.get(url=f"/api/v1/basket/show/blogger/order?blogger_area_id={blogger_area_id}")
            print(response.status)
            print(await response.json())
            return response.status, await response.json()

    async def project_moderation(self, params: dict):
        connector = TCPConnector(ssl=True, verify_ssl=True)
        async with ClientSession(base_url=domain, connector=connector) as session:
            response = await session.get(url="/api/v1/basket/show/blogger/moderation/order", params=params)
            print(response.status)
            print(await response.json())
            return response.status, await response.json()