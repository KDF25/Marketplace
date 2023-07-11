from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound,  MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.reply.common.common import ReplyStart
from keyboards.reply.common.user import ReplyUser
from looping import fastapi, pg
from model.user import User
from text.common.formEntityData import FormEntityData
from text.common.formIndividualData import FormIndividualData
from text.common.formPersonalData import FormPersonalData
from text.common.formSelfEmployedAccountData import FormSelfEmployedAccountData
from text.common.formSelfEmployedCardData import FormSelfEmployedCardData
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class PersonalDataAdvertiser(StatesGroup):

    personalDataAdvertiser_level1 = State()
    personalDataAdvertiser_level2 = State()
    logout_level1 = State()


    # menu personal data
    async def menu_personal_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            print(data)
            state_name = await self._exist_personal_data(message=message, data=data)
        await state.set_state(state=state_name)

    @staticmethod
    async def _prepare(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        inline = InlinePersonalData(language=data.get('lang'))
        return Lang, reply, inline

    @staticmethod
    async def _exist(token):
        json = await fastapi.get_active_legal(token=token)
        return json

    async def _exist_personal_data(self, message, data):
        json = await self._exist(token=data.get("token"))
        if json.get("type_legal") == "entity":
            state_name = "PersonalDataEntityAdvertiser:personalData_level1"
            data["entity"] = await func.get_entity(json=json)
            await self._entity(message=message, data=data)

        elif json.get("type_legal") == "individual":
            state_name = "PersonalDataIndividualAdvertiser:personalData_level1"
            data["individual"] = await func.get_individual(json=json)
            await self._individual(message=message, data=data)

        elif json.get("type_legal") == "self_employed_transit":
            state_name = "PersonalDataSelfEmployedCardAdvertiser:personalData_level1"
            data["selfEmployedCard"] = await func.get_self_employed_card(json=json)
            await self._self_employed_card(message=message, data=data)

        elif json.get("type_legal") == "self_employed":
            state_name = "PersonalDataSelfEmployedAccountAdvertiser:personalData_level1"
            data["selfEmployedAccount"] = await func.get_self_employed_account(json=json)
            await self._self_employed_account(message=message, data=data)

        else:
            state_name = "PersonalDataAdvertiser:personalDataAdvertiser_level2"
            await self._add_data(message=message, data=data)
        return state_name

    async def _entity(self,  message, data):
        form = FormEntityData(data=data.get("entity"), language=data.get('lang'), email=data.get("email"))
        await self._view_data(message, data,form)

    async def _individual(self,  message, data):
        form = FormIndividualData(data=data.get("individual"), language=data.get('lang'), email=data.get("email"))
        await self._view_data(message, data, form)

    async def _self_employed_account(self, message, data):
        form = FormSelfEmployedAccountData(data=data.get("selfEmployedAccount"), language=data.get('lang'), email=data.get("email"))
        await self._view_data(message, data, form)

    async def _self_employed_card(self, message, data):
        form = FormSelfEmployedCardData(data=data.get("selfEmployedCard"), language=data.get('lang'), email=data.get("email"))
        await self._view_data(message, data, form)

    async def _view_data(self, message, data, form):
        Lang, reply, inline = await self._prepare(data=data)
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.account,
                                          reply_markup=await reply.personal_data())
        await self._delete_message(message=message, data=data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_personal_data(),
                                          reply_markup=await inline.menu_personal_data())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    async def _add_data(self, message, data):
        Lang, reply, inline = await self._prepare(data=data)
        form = FormPersonalData(data=data)
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.account,
                                          reply_markup=await reply.personal_data())
        await self._delete_message(message=message, data=data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_personal_data(),
                                          reply_markup=await inline.menu_employment())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu add data
    async def menu_add_data(self, call: types.CallbackQuery, state: FSMContext):
        await self.personalDataAdvertiser_level2.set()
        async with state.proxy() as data:
            print(data)
            Lang, reply, inline = await self._prepare(data=data)
            await self._add(message=call,Lang=Lang, reply=reply, inline=inline, data=data)

    @staticmethod
    async def _delete_message(message: Union[types.Message, types.CallbackQuery], data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id_None'))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))

    async def _add(self, message: types.CallbackQuery, data, Lang, reply, inline):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.account,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(message=message, data=data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.personalData.common.choose,
                                          reply_markup=await inline.menu_employment(back=True))
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu logout
    async def menu_logout(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.logout_level1.set()
        async with state.proxy() as data:
            print(data)
            Lang, reply, inline = await self._prepare_logout(data=data)
            await self._logout(message=message,Lang=Lang, reply=reply, inline=inline, data=data)

    @staticmethod
    async def _prepare_logout(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyUser(language=data.get('lang'))
        inline = InlinePersonalData(language=data.get('lang'))
        return Lang, reply, inline

    async def _logout(self,  message: Union[types.Message, types.CallbackQuery], data, Lang, reply, inline):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.account,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(message=message, data=data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.personalData.common.logout,
                                          reply_markup=await inline.menu_logout())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu common start
    async def menu_common_start(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            print(data)
            Lang, reply, inline = await self._prepare_common(data=data)
            await pg.update_telegram_user(user_id=call.from_user.id, client_id=None, email=None)
            await self._common_start(message=call, Lang=Lang, reply=reply, data=data)
            data = User(lang=data.get("lang"))
        await state.set_data(data=data)
        await state.set_state("MenuCommon:start")

    @staticmethod
    async def _prepare_common(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyStart()
        inline = InlinePersonalData(language=data.get('lang'))
        return Lang, reply, inline

    async def _common_start(self, message: types.CallbackQuery, data, Lang, reply):
        await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.menu,
                               reply_markup=await reply.start())
        await self._delete_message(message=message, data=data)


    def register_handlers_personal_data(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_personal_data, text=Txt.menu.account,                                     state="MenuAdvertiser:menuAdvertiser_level1")
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=["PersonalDataEntityAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataIndividualAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataSelfEmployedAccountAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataSelfEmployedCardAdvertiser:personalData_level1",
                                                                                                                               self.personalDataAdvertiser_level2, self.logout_level1,
                                                                                                                               "FirstPlatformAdvertiser:firstPlatform_level15"])

        dp.register_callback_query_handler(self.menu_add_data, text="newData",                                          state=["PersonalDataEntityAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataIndividualAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataSelfEmployedAccountAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataSelfEmployedCardAdvertiser:personalData_level1"])
        dp.register_callback_query_handler(self.menu_add_data, text="back",                                             state=["AddDataEntityAdvertiser:addData_level1",
                                                                                                                               "AddDataIndividualAdvertiser:addData_level1",
                                                                                                                               "AddDataSelfEmployedAccountAdvertiser:addData_level1",
                                                                                                                               "AddDataSelfEmployedCardAdvertiser:addData_level1"])

        dp.register_message_handler(self.menu_logout, text=Txt.menu.logout,                                             state=["PersonalDataEntityAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataIndividualAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataSelfEmployedAccountAdvertiser:personalData_level1",
                                                                                                                               "PersonalDataSelfEmployedCardAdvertiser:personalData_level1",
                                                                                                                               "FirstPlatformAdvertiser:firstPlatform_level15", self.personalDataAdvertiser_level2])
        dp.register_callback_query_handler(self.menu_common_start, text="logout",                                       state=self.logout_level1)
