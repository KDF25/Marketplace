import json
from contextlib import suppress
from datetime import datetime, timedelta
from typing import Union
from datetime_now import dt_now
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, \
    MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from filters.form_order import IsSearch, IsPostLength, IsCommentLength, IsUrlButton
from keyboards.inline.advertiser.form_order import InlineFormOrderAdvertiser
from keyboards.reply.advertiser.advertiser import ReplyAdvertiser
from keyboards.reply.common.user import ReplyUser
from looping import fastapi
from model.calendar import CalendarModel
from model.form_order import FormOrderModel, PlatformList, ChannelModel, OtherModel, ChannelListModel, PostModel
from model.platform import Values, Params, GetPlatform
from text.advertiser.formOrder import FormOrder
from text.fuction.decoding import Decoding
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FormOrderAdvertiser(StatesGroup):
    formOrderAdvertiser_level1 = State()
    formOrderAdvertiser_level2 = State()
    formOrderAdvertiser_level3 = State()
    formOrderAdvertiser_level4 = State()
    formOrderAdvertiser_level5 = State()
    formOrderAdvertiser_level6 = State()
    formOrderAdvertiser_level7 = State()
    formOrderAdvertiser_level8 = State()

    category_level1 = State()
    parameters_level1 = State()
    network_level1 = State()

    lang_level1 = State()
    region_level1 = State()
    sex_level1 = State()
    age_level1 = State()

    current_platform_level1 = State()
    search_filters_level1 = State()
    find_level1 = State()

    category_level2 = State()
    parameters_level2 = State()
    lang_level2 = State()
    region_level2 = State()
    sex_level2 = State()
    age_level2 = State()

    url_level1 = State()
    media_level1 = State()
    comment_level1 = State()

    chanel_level1 = State()
    calendar_level1 = State()
    time_level_1 = State()

    order_level1 = State()



    @staticmethod
    async def _get_value(parameter_id: int, values: list):
        Dict = {}
        for i in values:
            Dict[i['id']] = i["name"]
        return Dict[parameter_id]

    # change Languages, regions, ages
    async def _change_parameter(self, parameter: dict, new_id: str):
        list_id = parameter.get("id")
        list_values = parameter.get("values")
        new_id = int(new_id.split("_")[1])
        new_value = await self._get_value(parameter_id=new_id, values=parameter.get("all_values"))
        if new_id not in list_id:
            list_id.append(new_id)
            list_values.append(new_value)
        elif new_id in list_id:
            list_id.remove(new_id)
            list_values.remove(new_value)

    @staticmethod
    async def _get_platform_list(data):
        Json = PlatformList(offset=data.get('formOrder').get('siteRequest').get('offset'),
                            limit=data.get('formOrder').get('siteRequest').get('limit'),
                            language=data.get('lang'),
                            channel=ChannelModel(category=data.get('formOrder').get('category').get('id'),
                                                 sex_ratio=data.get('formOrder').get('sex', 0),
                                                 age=data.get('formOrder').get('age').get('id'),
                                                 language=data.get('formOrder').get('platformLang').get('id'),
                                                 region=data.get('formOrder').get('regions').get('id')),
                            other=OtherModel(type_channel=data.get('formOrder').get('siteRequest').get('type_channel'),
                                             accommodation=data.get('formOrder').get('siteRequest').get('accommodation'),
                                             sorted_by=data.get('formOrder').get('siteRequest').get('sorted_by'),
                                             selected=data.get('formOrder').get('siteRequest').get('selected')))
        if data.get('formOrder').get('search') is not None:
            Json.update(PlatformList(word=data.get('formOrder').get('search')))
        json = await fastapi.get_platform_list(json=Json, token=data.get('token'))
        page = data.get('formOrder').get('siteRequest').get('offset') // data.get('formOrder').get('siteRequest').get('limit') + 1
        page = page if json['pages'] != 0 else 0
        data.get('formOrder')["channels"] = ChannelListModel(platformList=json['channels'], count=json['count'],
                                                             pages=json['pages'], page=page)
        return data

    @staticmethod
    async def _update_type_platform(data):
        params = Params(language=data.get('lang'), channel_type=data.get('formOrder').get('siteRequest').get('type_channel'))
        accommodations = await fastapi.get_channel_accommodations(params=params, token=data.get('token'))
        data.get('formOrder').get("platformTypes")["accommodations"] = accommodations.get("types")
        data.get('formOrder').get("siteRequest")["accommodation"] = accommodations.get("types")[0].get("id")

        # menu form order
    async def menu_form_order(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        message = message
        await self.formOrderAdvertiser_level1.set()
        async with state.proxy() as data:
            print(data)
            await self._callback_form_order(data=data)
            Lang, reply, inline, form = await self._prepare(data=data)
            if isinstance(message, types.Message):
                await self._form_order(message, Lang, reply, inline, form, data)
            elif isinstance(message, types.CallbackQuery):
                await self._form_order_back(message, inline, form)
            print(data)

    async def _callback_form_order(self, data):
        if data.get('formOrder') is None or data.get('formOrder') == {}:
            params = {"language": "rus"}
            types_platform = await fastapi.get_channel_types(params=params, token=data.get('token'))
            data["formOrder"] = FormOrderModel(platformTypes=Values(id=[1], all_values=types_platform.get("types")),
                                               category=Values(id=[], values=[]),
                                               platformLang=Values(id=[], values=[]),
                                               age=Values(id=[], values=[]),
                                               network=Values(id=[], values=[]),
                                               regions=Values(id=[], values=[]),
                                               siteRequest=OtherModel(type_channel=1, accommodation=1,
                                                                      sorted_by="subs_default", selected=[],
                                                                      offset=0, limit=Txt.limit.advertiser.formOrder),
                                               basket={"channels": []},
                                               selected=[])
            await self._update_type_platform(data=data)

    async def _prepare(self, data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyAdvertiser(language=data.get('lang'))
        status_parameters = await self._status_parameters(data)
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           status_parameters=status_parameters,
                                           status_network=len(data.get("formOrder", {}).get("network", {}).get("id", [])),
                                           status_category=len(data.get("formOrder", {}).get("category", {}).get("id", [])))
        form = FormOrder(data=data.get("formOrder"), language=data.get("lang"))
        return Lang, reply, inline, form

    @staticmethod
    async def _status_parameters(data):
        status_sex = 1 if data.get("formOrder", {}).get("sex") is not None else 0
        status_age = len(data.get("formOrder", {}).get("age", {}).get("id", []))
        status_lang = len(data.get("formOrder", {}).get("platformLang", {}).get("id", []))
        status_region = len(data.get("formOrder", {}).get("regions", {}).get("id", []))
        status_parameters = status_sex + status_age + status_lang + status_region
        return status_parameters

    @staticmethod
    async def _form_order(message, Lang, reply, inline, form, data):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.main_menu())
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_form_order(),
                                          reply_markup=await inline.menu_form_order())
        data['message_id'] = message1.message_id
        data['message_id_None'] = message2.message_id

    @staticmethod
    async def _form_order_back(message, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                        text=await form.menu_form_order(),  reply_markup=await inline.menu_form_order())

    # menu category
    async def menu_category(self, call: types.CallbackQuery, state: FSMContext):
        await self._state_category(await state.get_state())
        async with state.proxy() as data:
            await self._get_all_category(data=data)
            inline, form = await self._prepare_category(data=data)
            await self._category(call, form, inline)

    async def _state_category(self, state_name):
        if state_name == "FormOrderAdvertiser:formOrderAdvertiser_level1":
            await self.category_level1.set()
        elif state_name == "FormOrderAdvertiser:search_filters_level1":
            await self.category_level2.set()

    @staticmethod
    async def _prepare_category(data):
        form = FormOrder(data=data.get("formOrder"), language=data.get("lang"))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'),
                                           page=data.get("formOrder").get("category").get("page"),
                                           category=data.get("formOrder").get("category"))
        return inline, form

    @staticmethod
    async def _get_all_category(data):
        if data.get("formOrder", {}).get("category", {}).get("all_values") is None:
            params = Params(language=data.get('lang'), offset=0, limit=100)
            all_category = await fastapi.get_company_categories(params=params, token=data.get('token'))
            max_page = await func.max_page(units=all_category["types"])
            data.get("formOrder").get("category").update(Values(all_values=all_category["types"],
                                                                page=1, max_page=max_page))

    @staticmethod
    async def _category(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_category(), reply_markup=await inline.menu_category())

    # menu change category
    async def menu_change_category(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("formOrder").get("category"), new_id=call.data)
            inline, form = await self._prepare_category(data=data)
            await self._category(call, form, inline)

    # menu turn page category
    async def menu_category_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_category(data=data, call=call)
            inline, form = await self._prepare_category(data=data)
            await self._category(call, form, inline)

    @staticmethod
    async def _callback_category(data, call):
        page = data.get("formOrder").get("category").get("page")
        if call.data == "next" and page < data.get("formOrder").get("category").get("max_page"):
            data.get("formOrder").get("category")["page"] += 1
        elif call.data == "prev" and page > 1:
            data.get("formOrder").get("category")["page"] -= 1

    # menu network
    async def menu_network(self,  call: types.CallbackQuery, state: FSMContext):
        await self.network_level1.set()
        async with state.proxy() as data:
            await self._get_all_network(data=data)
            Lang, inline = await self._prepare_network(data=data)
            await self._network(call, Lang, inline)

    @staticmethod
    async def _prepare_network(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), network=data.get("formOrder").get("network"))
        return Lang, inline

    @staticmethod
    async def _get_all_network(data):
        if data.get("formOrder").get("network").get("all_values") is None:
            params = Params(language=data.get("lang"), offset=0, limit=40)
            all_kind = await fastapi.get_channel_types(params=params, token=data.get('token'))
            data.get("formOrder").get("network").update(Values(all_values=all_kind["types"]))

    @staticmethod
    async def _network(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.formOrder.change.network,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_kind())

    # menu change network
    async def menu_change_network(self,  call: types.CallbackQuery, state: FSMContext):
        await self.network_level1.set()
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("formOrder").get("network"), new_id=call.data)
            Lang, inline = await self._prepare_network(data=data)
            await self._network(call, Lang, inline)

    # menu parameters
    async def menu_parameters(self,  call: types.CallbackQuery, state: FSMContext):
        await self.parameters_level1.set()
        async with state.proxy() as data:
            form, inline = await self._prepare_change(data)
            await self._parameters(call, form, inline)

    async def menu_parameters_from_search(self,  call: types.CallbackQuery, state: FSMContext):
        await self.parameters_level2.set()
        async with state.proxy() as data:
            form, inline = await self._prepare_change(data)
            await self._parameters(call, form, inline)

    @staticmethod
    async def _prepare_change(data):
        inline = InlineFormOrderAdvertiser(language=data.get('lang'),
                                           status_sex=1 if data.get("formOrder").get("sex") is not None else 0,
                                           status_age=len(data.get("formOrder").get("age", {}).get("id", [])),
                                           status_lang=len(data.get("formOrder").get("platformLang", {}).get("id", [])),
                                           status_region=len(data.get("formOrder").get("regions", {}).get("id", [])))
        form = FormOrder(data=data.get("formOrder"), language=data.get("lang"))
        return form, inline

    @staticmethod
    async def _parameters(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_parameters(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_parameters())

    # menu language
    async def menu_lang(self, call: types.CallbackQuery, state: FSMContext):
        await self._state_lang(await state.get_state())
        async with state.proxy() as data:
            Lang, inline = await self._prepare_lang(data)
            await self._lang(call, Lang, inline)
            print(data)

    async def _state_lang(self, state_name):
        if state_name == "FormOrderAdvertiser:parameters_level1":
            await self.lang_level1.set()
        elif state_name == "FormOrderAdvertiser:parameters_level2":
            await self.lang_level2.set()

    async def _prepare_lang(self, data):
        await self._get_all_lang(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           platform_lang=data.get("formOrder").get("platformLang"))
        return Lang, inline

    @staticmethod
    async def _get_all_lang(data):
        if data.get("formOrder").get("platformLang").get("all_values") is None:
            params = Params(language=data.get('lang'), offset=0, limit=40)
            all_platformLang = await fastapi.get_channel_languages(params=params, token=data.get('token'))
            data.get("formOrder")["platformLang"].update(Values(all_values=all_platformLang["types"]))

    @staticmethod
    async def _lang(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.formOrder.change.lang,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_lang())

    # menu change language
    async def menu_change_lang(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("formOrder").get("platformLang"), new_id=call.data)
            Lang, inline = await self._prepare_lang(data)
            await self._lang(call, Lang, inline)

    # menu region
    async def menu_region(self, call: types.CallbackQuery, state: FSMContext):
        await self._state_region(await state.get_state())
        async with state.proxy() as data:
            Lang, inline = await self._prepare_region(data)
            await self._region(call, Lang, inline)

    async def _state_region(self, state_name):
        if state_name == "FormOrderAdvertiser:parameters_level1":
            await self.region_level1.set()
        elif state_name == "FormOrderAdvertiser:parameters_level2":
            await self.region_level2.set()

    async def _prepare_region(self, data):
        await self._get_all_regions(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), regions=data.get("formOrder").get("regions"))
        return Lang, inline

    @staticmethod
    async def _get_all_regions(data):
        if data.get("formOrder").get("regions").get("all_values") is None:
            params = Params(language=data.get('lang'), offset=0, limit=40)
            all_regions = await fastapi.get_regions(params=params, token=data.get('token'))
            data.get("formOrder")["regions"].update(Values(all_values=all_regions["types"]))

    @staticmethod
    async def _region(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.formOrder.change.region,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_region())

    # menu change region
    async def menu_change_region(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("formOrder").get("regions"), new_id=call.data)
            Lang, inline = await self._prepare_region(data)
            await self._region(call, Lang, inline)

    # menu sex
    async def menu_sex(self, call:  types.CallbackQuery, state: FSMContext):
        await self._state_sex(await state.get_state())
        async with state.proxy() as data:
            Lang, reply, inline, form = await self._prepare(data=data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.formOrder.change.sex, reply_markup=await inline.menu_sex())

    async def _state_sex(self, state_name):
        if state_name == "FormOrderAdvertiser:parameters_level1":
            await self.sex_level1.set()
        elif state_name == "FormOrderAdvertiser:parameters_level2":
            await self.sex_level2.set()

    # menu get sex
    async def menu_get_sex(self, call: types.CallbackQuery, state: FSMContext):
        await self._state_get_sex(await state.get_state())
        async with state.proxy() as data:
            await self._callback_sex(data, call)
            form, inline = await self._prepare_change(data)
            await self._parameters(call, form, inline)

    async def _state_get_sex(self, state_name):
        if state_name == "FormOrderAdvertiser:sex_level1":
            await self.parameters_level1.set()
        elif state_name == "FormOrderAdvertiser:sex_level2":
            await self.parameters_level2.set()

    @staticmethod
    async def _callback_sex(data, call):
        data.get('formOrder')["sex"] = int(call.data.split("_")[1])
        data.get("formOrder")["sex_value"] = await Decoding(language=data.get("lang"), token=data.get("token"),
                                                            param_id=data.get("formOrder").get("sex")).get_sex()

    # menu age
    async def menu_age(self, call: types.CallbackQuery, state: FSMContext):
        await self._state_age(await state.get_state())
        async with state.proxy() as data:
            Lang, inline = await self._prepare_age(data)
            await self._age(call, Lang, inline)

    async def _state_age(self, state_name):
        if state_name == "FormOrderAdvertiser:parameters_level1":
            await self.age_level1.set()
        elif state_name == "FormOrderAdvertiser:parameters_level2":
            await self.age_level2.set()

    async def _prepare_age(self, data):
        await self._get_all_ages(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), age=data.get("formOrder").get("age"))
        return Lang, inline

    @staticmethod
    async def _get_all_ages(data):
        if data.get("formOrder").get("age").get("all_values") is None:
            params = Params(language=data.get('lang'))
            all_ages = await fastapi.get_channel_age_ratios(params=params, token=data.get('token'))
            data.get("formOrder")["age"].update(Values(all_values=all_ages["types"]))

    @staticmethod
    async def _age(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.formOrder.change.age,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_age())

    # menu change age
    async def menu_change_age(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("formOrder").get("age"), new_id=call.data)
            Lang, inline = await self._prepare_age(data)
            await self._age(call, Lang, inline)

    # menu all platform
    async def menu_all_platform(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_category(data, call)

    async def _check_category(self, data, call):
        if len(data.get("formOrder").get("category").get("id")) == 0:
            Lang = Txt.language[data.get('lang')]
            await call.answer(text=Lang.alert.advertiser.category, show_alert=True)
        else:
            await self.formOrderAdvertiser_level2.set()
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform(call, data, Lang, reply, inline, form)

    @staticmethod
    async def _prepare_all_platform(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyAdvertiser(language=data.get('lang'))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           all_channels=data.get('formOrder').get('channels'),
                                           search=data.get('formOrder').get('search'),
                                           accommodation=data.get('formOrder').get('platformTypes').get(
                                               "accommodations"),
                                           accommodation_filter=data.get("formOrder").get("siteRequest").get(
                                               "accommodation"),
                                           platform_types=data.get("formOrder").get("platformTypes"),
                                           main_filter=data.get("formOrder").get("siteRequest").get('sorted_by'))
        form = FormOrder(data=data.get("formOrder"), language=data.get("lang"))
        return Lang, reply, inline, form

    @staticmethod
    async def _delete_message(call, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id_None'))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))

    async def _all_platform(self, call, data, Lang, reply, inline, form):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.menu_basket())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form.menu_all_platform(),
                                          reply_markup=await inline.menu_all_platform(),
                                          disable_web_page_preview=True)
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu change accommodation
    async def menu_change_accommodation(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_accommodation(call, data)
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform_filters(call, inline, form)

    @staticmethod
    async def _change_accommodation(call, data):
        List = []
        current = int(call.data.split("_")[1])
        for accommodation in data.get('formOrder').get("platformTypes").get("accommodations"):
            List.append(accommodation.get('id'))
        try:
            new = List[List.index(current) + 1]
        except IndexError:
            new = List[0]
        data.get("formOrder").get("siteRequest")["accommodation"] = new

    async def menu_change_platform_type(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_platform_type(call, data)
            await self._update_type_platform(data=data)
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform_filters(call, inline, form)

    @staticmethod
    async def _change_platform_type(call, data):
        platform = int(call.data.split("_")[1])
        data.get('formOrder').get("platformTypes")["id"] = [platform]
        data.get('formOrder').get("siteRequest")["type_channel"] = platform

    # menu all platform turn
    async def menu_all_platform_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_all_platform(data=data, call =call)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform_filters(call, inline, form)

    async def _callback_all_platform(self, call, data):
        limit = data.get('formOrder').get('siteRequest').get('limit')
        pages = data.get('formOrder').get('channels').get('pages')
        page = data.get('formOrder').get('channels').get('page')
        if call.data == "prev" and page > 1:
            data.get('formOrder').get('siteRequest')['offset'] -= limit
            data.get('formOrder').get('channels')['page'] -= 1
            await self._get_platform_list(data=data)
        elif call.data == "next" and page < pages:
            data.get('formOrder').get('siteRequest')['offset'] += limit
            data.get('formOrder').get('channels')['page'] += 1
            await self._get_platform_list(data=data)

    @staticmethod
    async def _all_platform_filters(call, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_all_platform(),
                                        message_id=call.message.message_id, disable_web_page_preview=True,
                                        reply_markup=await inline.menu_all_platform())

    # menu menu change sorted
    async def menu_change_sorted(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data.get("formOrder").get("siteRequest")['sorted_by'] = call.data
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform_filters(call, inline, form)

    # menu current platform
    async def menu_current_platform(self, call: types.CallbackQuery, state: FSMContext):
        await self.current_platform_level1.set()
        async with state.proxy() as data:
            await self._get_current_platform(call, data)
            Lang, reply, inline, form = await self._prepare_current_platform(data=data)
            await self._current_platform(call, data, Lang, reply, inline, form)

    @staticmethod
    async def _get_current_platform(call, data):
        params = GetPlatform(language=data.get("lang"), area_id=int(call.data.split("_")[1]))
        json = await fastapi.get_area(token=data.get("token"), params=params)
        data.get('formOrder')["current_platform"] = json
        current_accommodation = [data.get('formOrder').get('siteRequest').get('accommodation')]
        data.get('formOrder').get("current_platform")['current_accommodation'] = current_accommodation

    @staticmethod
    async def _prepare_current_platform(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyAdvertiser(language=data.get('lang'))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           accommodation=data.get('formOrder').get('current_platform'))
        form = FormOrder(data=data.get("formOrder").get('current_platform'), language=data.get("lang"))
        return Lang, reply, inline, form

    async def _current_platform(self, call, data, Lang, reply, inline, form):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form.menu_current_platform(),
                                          reply_markup=await inline.menu_current_platform(),
                                          disable_web_page_preview=True)
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu change current platform accommodation
    async def menu_change_current_platform_accommodation(self, call: types.CallbackQuery, state: FSMContext):
        new_id = int(call.data.split('_')[1])
        async with state.proxy() as data:
            data.get('formOrder').get('current_platform')['current_accommodation'] = [new_id]
            Lang, reply, inline, form = await self._prepare_current_platform(data=data)
            await self._change_current_platform_accommodation(call, inline, form)

    @staticmethod
    async def _change_current_platform_accommodation(call, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_current_platform(),
                                        message_id=call.message.message_id, disable_web_page_preview=True,
                                        reply_markup=await inline.menu_current_platform())

    # menu add basket
    async def menu_add_basket(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_max_basket_len(call, data)

    async def _check_max_basket_len(self, call, data):
        if len(data.get('formOrder').get("basket").get("channels")) <= Txt.limit.advertiser.basket:
            await self.formOrderAdvertiser_level2.set()
            data.get('formOrder').get("basket").get("channels").append(data.get('formOrder').get("current_platform"))
            data.get('formOrder').get("siteRequest").get("selected").append(data.get('formOrder').get("current_platform").get('id'))
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform(call, data, Lang, reply, inline, form)
        else:
            Lang = Txt.language[data.get('lang')]
            await call.answer(text=Lang.alert.advertiser.maxBasket, show_alert=True)

    # menu search & filters
    async def menu_search_filters(self, call: types.CallbackQuery, state: FSMContext):
        await self.search_filters_level1.set()
        async with state.proxy() as data:
            await self._callback_search_filters(call, data)

    async def _callback_search_filters(self, call, data):
        Lang, reply, inline, form = await self._prepare(data=data)
        if call.data == "search":
            await self._search_filters(call, inline, form)
        elif call.data == "back" or call.data == "confirm":
            await self._search_filters_back(call, inline, form, data)

    @staticmethod
    async def _search_filters(call, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_search_filters(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_search_filters())

    @staticmethod
    async def _search_filters_back(call, inline, form, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form.menu_search_filters(),
                                          reply_markup=await inline.menu_search_filters())
        data['message_id'] = message1.message_id

    # menu search
    async def menu_search(self, call: types.CallbackQuery, state: FSMContext):
        await self.find_level1.set()
        async with state.proxy() as data:
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._search(call, inline, Lang)

    @staticmethod
    async def _search(call, inline, Lang):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.formOrder.find,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # menu get search
    async def menu_get_search(self, message: types.Message, state: FSMContext):
        await self.formOrderAdvertiser_level2.set()
        async with state.proxy() as data:
            data.get('formOrder')['search'] = str(message.text)
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._all_platform(message, data, Lang, reply, inline, form)

    # menu delete search
    async def menu_delete_search(self, call: types.CallbackQuery, state: FSMContext):
        await self.formOrderAdvertiser_level2.set()
        async with state.proxy() as data:
            data.get('formOrder').pop('search')
            await self._get_platform_list(data=data)
            Lang, reply, inline, form = await self._prepare_all_platform(data)
            await self._delete_search(call, inline, form)

    @staticmethod
    async def _delete_search(call, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_all_platform(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_all_platform(),
                                        disable_web_page_preview=True)

    # menu basket
    async def menu_basket(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._check_basket(data, message)

    async def _check_basket(self, data, message):
        Lang, reply, inline, form = await self._prepare_basket(data)
        if len(data.get('formOrder').get("basket").get("channels")) != 0:
            await self.formOrderAdvertiser_level3.set()
            await self._basket(message, inline, form, reply, Lang, data)
            Json = await func.add_basket(data=data)
            await fastapi.add_unpaid_basket(json=Json, token=data.get("token"))
        else:
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
            message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.emptyBasket,
                                              reply_markup=await inline.menu_back())
            data["message_id"] = message1.message_id

    @staticmethod
    async def _prepare_basket(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyAdvertiser(language=data.get('lang'))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           platform_list=data.get('formOrder').get("basket").get("channels"))
        form = FormOrder(data=data.get('formOrder').get("basket"), language=data.get("lang"))
        return Lang, reply, inline, form

    async def _basket(self, call, inline, form, reply, Lang, data):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.menu_task(login=data['email'], password=data['password']))
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form.menu_basket(),
                                          reply_markup=await inline.menu_basket(token=data['token']['access_token'],
                                                                                user_id=call.from_user.id),
                                          disable_web_page_preview=True)
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu delete basket
    async def menu_delete_basket(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._delete_channel(call, data)
            Json = await func.add_basket(data=data)
            await fastapi.add_unpaid_basket(json=Json, token=data.get("token"))
            await self._check_basket2(call, data, state)

    @staticmethod
    async def _delete_channel(call, data):
        data.get('formOrder').get("siteRequest").get("selected").remove(int(call.data.split('_')[1]))
        for platform in data.get('formOrder').get("basket").get("channels"):
            if platform.get('id') == int(call.data.split('_')[1]):
                data.get('formOrder').get("basket").get("channels").remove(platform)

    async def _check_basket2(self, call, data, state):
        Lang, reply, inline, form = await self._prepare_basket(data)
        if len(data.get('formOrder').get("basket").get("channels")) != 0:
            await self._delete_basket(call, inline, form, data)
        else:
            await state.set_state('MenuAdvertiser:menuAdvertiser_level1')
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                reply = ReplyUser(language=data.get('lang'))
                await bot.send_message(chat_id=call.from_user.id, text=Lang.alert.advertiser.emptyBasket,
                                       reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _delete_basket(call, inline, form, data):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_basket(),
                                        message_id=call.message.message_id, disable_web_page_preview=True,
                                        reply_markup=await inline.menu_basket())

    # menu name campaign
    async def menu_campaign(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await self._check_len_basket(message, data)


    async def menu_campaign_web_app(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        print('333')
        async with state.proxy() as data:
            await self.formOrderAdvertiser_level4.set()
            data['formOrder'] = {}
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._campaign(message, inline, reply, Lang, data)
            status, Json = await fastapi.get_unpaid_basket(token=data.get("token"), language=data.get("lang"))
            await self._unpack_basket(data, Json)
            await self._total_cost(data)
            # await self._check_len_basket(message, data)

    async def _unpack_basket(self, data, Json):
        await self._callback_form_order(data)
        await self._get_all_category(data)
        await self._change_parameter(parameter=data.get("formOrder").get("category"), new_id="category_1")
        await self._get_unpaid_basket(data, Json)

    @staticmethod
    async def _get_unpaid_basket(data, Json):
        data.get('formOrder').get("basket")["channels"] = Json.get("channels")
        selected = []
        for channel in Json.get("channels"):
            selected.append(channel.get("id"))
        data.get('formOrder').get("siteRequest")["selected"] = selected


    async def _check_len_basket(self, message, data):
        if len(data.get("formOrder").get('basket').get("channels")) != 0:
            await self.formOrderAdvertiser_level4.set()
            Json = await func.add_basket(data=data)
            await fastapi.add_unpaid_basket(json=Json, token=data.get("token"))
            await self._total_cost(data)
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._campaign(message, inline, reply, Lang, data)
        else:
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

    @staticmethod
    async def _total_cost(data):
        price = 0
        for channel in data.get("formOrder").get('basket').get("channels"):
            for accommodation in channel.get("area_accommodation"):
                if accommodation.get("id") in channel.get('current_accommodation'):
                    price += accommodation.get("price")
        cost = await func.commission(price=price)
        data.get("formOrder").get("basket")["total_cost"] = cost

    async def _campaign(self, call, inline, reply, Lang, data):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.formOrder.campaign,
                                          reply_markup=await reply.main_campaign(login=data['email'], password=data['password']))
        await self._delete_message(call, data)
        # message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.formOrder.campaign)
        data['message_id_None'] = message2.message_id
        # data['message_id'] = message1.message_id

    # menu get name campaign
    async def menu_name_campaign(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.formOrderAdvertiser_level5.set()
        async with state.proxy() as data:
            if isinstance(message, types.Message):
                await self._callback_campaign(message, data)

            Lang, reply, inline, form = await self._prepare(data=data)
            await self._name_campaign(message, data, form, inline, reply, Lang)

    @staticmethod
    async def _callback_campaign(message, data):
        if data.get("formOrder").get('campaign') is None:
            data.get("formOrder")["campaign"] = {}
        data.get("formOrder").get("campaign")["name"] = message.text
        json = PostModel(name=data.get("formOrder").get("campaign").get("name"))
        json = await fastapi.create_order(json=json, token=data.get("token"))
        data.get("formOrder").get("campaign")['order_id'] = json.get("order_id")

    # @staticmethod
    async def _name_campaign(self, message, data, form, inline, reply, Lang):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.formOrder, reply_markup=await reply.main_menu())
        await self._delete_message(message, data)
        # with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
        #     await bot.delete_message(chat_id=message.from_user.id, message_id=data.get("message_id"))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_campaign_text(),
                                          reply_markup=await inline.menu_back(), disable_web_page_preview=True)
        data['message_id'] = message1.message_id
        data['message_id_None'] = message2.message_id

    # menu_post
    async def menu_post(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            if isinstance(message, types.Message):
                await self._post_content_type(data, message)
            await self._post_common(data, message)
            await self._post_type(data, message)

    @staticmethod
    async def _prepare_post(data):
        reply = ReplyAdvertiser(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        form = FormOrder(data=data.get("formOrder"), language=data.get("lang"))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           url_buttons=data.get("formOrder").get("campaign").get("buttons"),
                                           media_button=bool(data.get("formOrder").get("campaign").get("media")),
                                           comment_button=bool(data.get("formOrder").get("campaign").get("comment")))
        return Lang, reply, inline, form

    @staticmethod
    async def _post_content_type(data, call):
        data.get("formOrder").get("campaign")["post"] = {}
        try:
            text = call.html_text
        except TypeError:
            text = None
        if len(call.photo) != 0:
            data.get("formOrder").get("campaign").get("post")["type"] = "photo"
            data.get("formOrder").get("campaign").get("post")["file_id"] = call.photo[-1].file_id
        elif call.video is not None:
            data.get("formOrder").get("campaign").get("post")["type"] = "video"
            data.get("formOrder").get("campaign").get("post")["file_id"] = call.video.file_id
        elif call.text is not None:
            data.get("formOrder").get("campaign").get("post")["type"] = "text"
        data.get("formOrder").get("campaign").get("post")["caption"] = text

    async def _post_type(self, data, message):
        Lang, reply, inline, form = await self._prepare_post(data)
        Type = data.get("formOrder").get("campaign").get("post").get("type")
        await self.formOrderAdvertiser_level6.set()
        if Type == "photo":
            await self._post_photo(message, Lang, inline, form, data)
        elif Type == "video":
            await self._post_video(message, form, inline, Lang, data)
        elif Type == "text":
            await self._post_text(message, form, inline, Lang, data)

    async def _post_common(self, data, call):
        Lang, reply, inline, form = await self._prepare_post(data)
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.menu_accept())
        await self._delete_message(call, data)
        data['message_id_None'] = message2.message_id

    @staticmethod
    async def _post_photo(message, Lang, inline, form, data):
        post = data.get("formOrder").get("campaign").get("post")
        text = await form.menu_post(caption=post.get("caption"),
                                    comment=data.get("formOrder").get("campaign").get("comment"))
        text += "\n\n" + Lang.formOrder.alright
        message1 = await bot.send_photo(chat_id=message.from_user.id, photo=post.get("file_id"), parse_mode="html",
                                        caption=text, reply_markup=await inline.menu_post())
        data['message_id'] = message1.message_id

    @staticmethod
    async def _post_video(message, form, inline, Lang, data):
        post = data.get("formOrder").get("campaign").get("post")
        text = await form.menu_post(caption=post.get("caption"),
                                    comment=data.get("formOrder").get("campaign").get("comment"))
        text += "\n\n" + Lang.formOrder.alright
        message1 = await bot.send_video(chat_id=message.from_user.id, video=post.get("file_id"), parse_mode="html",
                                        caption=text, reply_markup=await inline.menu_post())
        data['message_id'] = message1.message_id

    @staticmethod
    async def _post_text(message, form, inline, Lang, data):
        post = data.get("formOrder").get("campaign").get("post")
        text = await form.menu_post(caption=post.get("caption"),
                                    comment=data.get("formOrder").get("campaign").get("comment"))
        text += "\n\n" + Lang.formOrder.alright
        message1 = await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode="html",
                                          reply_markup=await inline.menu_post())
        data['message_id'] = message1.message_id

    # menu url
    async def menu_url(self, call: types.CallbackQuery, state: FSMContext):
        await self.url_level1.set()
        async with state.proxy() as data:
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._url(call, inline, reply, Lang, data)

    async def _url(self, call, inline, reply, Lang, data):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.formOrder.url,
                                          reply_markup=await inline.menu_back())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu get url
    async def menu_get_url(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await self._url_buttons(message, data)
            await self._post_common(data, message)
            await self._post_type(data, message)

    @staticmethod
    async def _url_buttons(message, data):
        buttons = message.text
        buttons = [i.split("|") for i in buttons.split("\n")]
        data.get("formOrder").get("campaign")["buttons"] = buttons
        data.get("formOrder").get("campaign")["BUTTONS"] = message.text

    # menu_media_files
    async def menu_media_files(self, call: types.CallbackQuery, state: FSMContext):
        await self.media_level1.set()
        async with state.proxy() as data:
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._media_files(call, inline, reply, Lang, data)

    async def _media_files(self, call, inline, reply, Lang, data):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.formOrder.media,
                                          reply_markup=await inline.menu_back())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu get url
    async def menu_get_media(self, message: types.Message, state: FSMContext):
        print(message)
        async with state.proxy() as data:
            await self._media_type(message, data)
            await self._post_common(data, message)
            await self._post_type(data, message)

    @staticmethod
    async def _media_type(call, data):
        data.get("formOrder").get("campaign")["media"] = {}
        if len(call.photo) != 0:
            data.get("formOrder").get("campaign").get("media")["type"] = "photo"
            data.get("formOrder").get("campaign").get("media")["file_id"] = call.photo[-1].file_id
        elif call.video is not None:
            data.get("formOrder").get("campaign").get("media")["type"] = "video"
            data.get("formOrder").get("campaign").get("media")["file_id"] = call.video.file_id
        elif call.document is not None:
            data.get("formOrder").get("campaign").get("media")["type"] = "document"
            data.get("formOrder").get("campaign").get("media")["file_id"] = call.document.file_id

    # menu_comment
    async def menu_comment(self, call: types.CallbackQuery, state: FSMContext):
        await self.comment_level1.set()
        async with state.proxy() as data:
            Lang, reply, inline, form = await self._prepare(data=data)
            await self._comment(call, inline, reply, Lang, data)

    async def _comment(self, call, inline, reply, Lang, data):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.formOrder.comment,
                                          reply_markup=await inline.menu_back())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    # menu get comment
    async def menu_get_comment(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data.get("formOrder").get("campaign")["comment"] = message.text
            await self._post_common(data, message)
            await self._post_type(data, message)

    # menu delete url
    async def menu_delete_url(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data.get("formOrder").get("campaign").pop("buttons")
            await self._delete_type(call, data)

    # menu delete comment
    async def menu_delete_comment(self,call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data.get("formOrder").get("campaign").pop("comment")
            await self._delete_type(call, data)

    # menu delete media
    async def menu_delete_media_files(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            print("media", data)
            data.get("formOrder").get("campaign").pop("media")
            await self._delete_type(call, data)

    async def _delete_type(self, call, data):
        await self.formOrderAdvertiser_level6.set()
        Type = data.get("formOrder").get("campaign").get("post").get("type")
        Lang, reply, inline, form = await self._prepare_post(data)
        if Type == "photo":
            await self._delete_photo(call, inline,Lang, form, data)
        elif Type == "video":
            await self._delete_video(call, inline,Lang, form, data)
        elif Type == "text":
            await self._delete_text(call, inline,Lang, form, data)

    @staticmethod
    async def _delete_photo(call, inline,Lang, form, data):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            post = data.get("formOrder").get("campaign").get("post")
            text = await form.menu_post(caption=post.get("caption"),
                                        comment=data.get("formOrder").get("campaign").get("comment"))
            text += "\n\n" + Lang.formOrder.alright
            await bot.edit_message_caption(chat_id=call.from_user.id, message_id=data.get("message_id"),
                                           caption=text, parse_mode="html", reply_markup=await inline.menu_post())

    @staticmethod
    async def _delete_video(call, inline, Lang, form, data):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            post = data.get("formOrder").get("campaign").get("post")
            text = await form.menu_post(caption=post.get("caption"),
                                        comment=data.get("formOrder").get("campaign").get("comment"))
            text += "\n\n" + Lang.formOrder.alright
            await bot.edit_message_caption(chat_id=call.from_user.id, message_id=data.get("message_id"),
                                           caption=text, parse_mode="html", reply_markup=await inline.menu_post())

    @staticmethod
    async def _delete_text(call, inline, Lang, form, data):
        with suppress(MessageNotModified, MessageToEditNotFound):
            post = data.get("formOrder").get("campaign").get("post")
            text = await form.menu_post(caption=post.get("caption"),
                                        comment=data.get("formOrder").get("campaign").get("comment"))
            text += "\n\n" + Lang.formOrder.alright
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=data.get("message_id"),
                                        text=text, parse_mode="html", reply_markup=await inline.menu_post())

    # menu preview
    async def menu_all_dates(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.formOrderAdvertiser_level7.set()
        async with state.proxy() as data:
            Lang, reply, inline, form = await self._prepare_basket(data)
            print("get")

            # if data.get("formOrder").get("campaign").get("media", {}).get("file_id") is not None:
            #     type_file = "document"
            #     file_id = data.get("formOrder").get("campaign").get("media").get("file_id", "")
            #     json = PostModel(file_id=file_id, type_file=type_file,
            #                      order_id=data.get("formOrder").get("campaign").get("order_id"))
            #
            #     await fastapi.sender(json=json, token=data.get("token"))

            if isinstance(message, types.Message):
                await self._all_dates(message, data,  Lang, form, reply, inline)
            if isinstance(message, types.CallbackQuery):
                await self._all_dates_back(message, data, inline, form)

    async def _all_dates(self, call, data, Lang, form, reply, inline):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id,
                                          text=await form.menu_all_dates(campaign_name=data.get("formOrder").get("campaign").get("name")),
                                          reply_markup=await inline.menu_all_dates())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    @staticmethod
    async def _all_dates_back(call, data, inline, form):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_all_dates(campaign_name=data.get("formOrder").get("campaign").get("name")),
                                        reply_markup=await inline.menu_all_dates())

    # menu calendar
    async def menu_calendar(self, call: types.CallbackQuery, state: FSMContext):
        await self.calendar_level1.set()
        async with state.proxy() as data:
            await self._callback_calendar(call, data)
            await self._get_info_month(data)
            form, inline = await self._prepare_calendar(data)
            await self._calendar(call, data, form, inline)

    @staticmethod
    async def _get_info_month(data):
        area_id = data.get('formOrder').get('current_datetime').get('id')
        date = data.get('formOrder').get('current_datetime').get('date')
        date = datetime.strptime(date, "%d.%m.%Y")
        params = CalendarModel(area_id=area_id, year=date.year, month=date.month)
        json = await fastapi.get_info_month(token=data.get('token'), params=params)
        data.get('formOrder').get('current_datetime')["calendar"] = [day.get("date") for day in json.get("days")]

    @staticmethod
    async def _callback_calendar(call, data):
        if call.data != "back":
            now = dt_now.now()
            date = datetime.strftime(datetime(year=now.year, month=now.month, day=now.day), "%d.%m.%Y")
            data.get('formOrder')['current_datetime'] = {"id": int(call.data.split('_')[1]), "date": date, "time": [], "calendar": []}

    @staticmethod
    async def _prepare_calendar(data):
        form = FormOrder(language=data.get("lang"))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           date=data.get('formOrder').get('current_datetime').get("date"),
                                           calendar_list=data.get('formOrder').get('current_datetime').get("calendar"))
        return form, inline

    @staticmethod
    async def _calendar(call, data, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_calendar(campaign_name=data.get("formOrder").get("campaign").get("name")),
                                        reply_markup=await inline.menu_calendar())

    # menu calendar turn
    async def menu_calendar_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._calendar_turn(call, data)
            form, inline = await self._prepare_calendar(data)
            await self._calendar(call, data, form, inline)

    @staticmethod
    async def _calendar_turn(call, data):
        date = await func.calendar(date=data.get('formOrder').get('current_datetime').get("date"), turn=call.data)
        data.get('formOrder')['current_datetime'].update({"date": date})

    # menu busy day
    async def menu_calendar_busy(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            Lang = Txt.language[data.get('lang')]
            await call.answer(text=Lang.alert.advertiser.busy, show_alert=True)

    # menu time
    async def menu_time(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_date(call, data)

    async def _check_date(self, call, data):
        if datetime.strptime(call.data.split('_')[1], "%d.%m.%Y").date() >= dt_now.now().date() + timedelta(days=0):
            await self._valid_date(call, data)
        else:
            Lang = Txt.language[data.get('lang')]
            await call.answer(text=Lang.alert.common.calendar, show_alert=True)

    async def _valid_date(self, call, data):
        await self.time_level_1.set()
        data.get('formOrder').get('current_datetime')["date"] = call.data.split('_')[1]
        data.get('formOrder').get('current_datetime')["time"] = []
        times = await self._get_time(data)
        form, inline = await self._prepare_time(data, times)
        await self._time(call, data, form, inline)

    async def _get_time(self, data):
        for platform in data.get('formOrder').get("basket").get("channels"):
            if platform.get('id') == int(data.get('formOrder').get("current_datetime").get('id')) \
                    and platform.get('date') == data.get('formOrder').get("current_datetime").get('date'):
                default = data.get('formOrder').get('current_datetime').get("time")
                times = platform.get('time', default)
                data.get('formOrder').get('current_datetime')['time'] = times
                break
        else:
            times = data.get('formOrder').get('current_datetime').get("time")
        return times

    @staticmethod
    async def _prepare_time(data, times):
        form = FormOrder(language=data.get("lang"))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"), time=times)
        return form, inline

    @staticmethod
    async def _time(call, data, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.menu_time(campaign_name=data.get("formOrder").get("campaign").get("name")),
                                        reply_markup=await inline.menu_time())

    # menu time change
    async def menu_change_time(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._time_change_exist(call, data)
            form, inline = await self._prepare_time(data, data.get('formOrder').get('current_datetime')['time'])
            await self._time(call, data, form, inline)

    async def _time_change_exist(self, call, data):
        time = str(call.data.split('_')[1])
        for platform in data.get('formOrder').get("basket").get("channels"):
            if platform.get('id') == int(data.get('formOrder').get("current_datetime").get('id')) \
                    and platform.get('time') is not None \
                    and platform.get('date') == data.get('formOrder').get("current_datetime").get('date'):
                times = data.get('formOrder').get('current_datetime').get('time')
                times = await func.time_change(time=time, times=times)
                platform['time'] = times
                data.get('formOrder').get('current_datetime')['time'] = times
                break
        else:
            await self._time_change_new(call, data)

    @staticmethod
    async def _time_change_new(call, data):
        time = str(call.data.split('_')[1])
        times = data.get('formOrder').get('current_datetime').get('time')
        times = await func.time_change(time=time, times=times)
        data.get('formOrder').get('current_datetime')['time'] = times

    # menu all time
    async def menu_all_time(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._time_all_exist(data)
            form, inline = await self._prepare_time(data, data.get('formOrder').get('current_datetime')['time'])
            await self._time(call, data, form, inline)
        print(data)

    async def _time_all_exist(self, data):
        for platform in data.get('formOrder').get("basket").get("channels"):
            if platform.get('id') == int(data.get('formOrder').get("current_datetime").get('id')) \
                    and platform.get('time') is not None \
                    and platform.get('date') == data.get('formOrder').get("current_datetime").get('date'):
                if len(platform.get('time')) == 8:
                    times = []
                else:
                    times = await self._all_time()
                platform['time'] = times
                data.get('formOrder').get('current_datetime')['time'] = times
                break
        else:
            await self._time_all_new(data)

    async def _time_all_new(self, data):
        if len(data.get('formOrder').get('current_datetime').get("time", [])) == 8:
            times = []
        else:
            times = await self._all_time()
        data.get('formOrder').get('current_datetime')['time'] = times

    @staticmethod
    async def _all_time():
        times = [f"{i}:00 - {i + 3}:00" for i in range(0, 21, 3)]
        times.append("21:00 - 23:59")
        return times

    # menu get day
    async def menu_get_day(self, call: types.CallbackQuery, state: FSMContext):
        await self.formOrderAdvertiser_level7.set()
        async with state.proxy() as data:
            await self._get_day(data)
            Lang, reply, inline, form = await self._prepare_basket(data)
            await self._all_dates_back(call, data, inline, form)

    async def _get_day(self, data):
        for platform in data.get('formOrder').get("basket").get("channels"):
            if platform.get('id') == int(data.get('formOrder').get("current_datetime").get('id')):
                platform['date'] = data.get('formOrder').get("current_datetime").get('date')
                time = data.get('formOrder').get("current_datetime").get('time')
                all_time = await self._all_time()
                time = time if time is not None else all_time
                platform['time'] = time
                break

    # menu last preview
    async def menu_last_preview(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_all_dates(call, data)

    async def _check_all_dates(self,call,  data):
        Lang, reply, inline, form = await self._prepare_basket(data)
        for platform in data.get('formOrder').get("basket").get("channels"):
            if platform.get('date') is None:
                await call.answer(text=Lang.alert.advertiser.allDates, show_alert=True)
                break
            elif platform.get('date') is not None and len(platform.get('time')) == 0:
                platform['time'] = await self._all_time()
        else:
            await self._last_preview(call, data, form, inline)

    async def _last_preview(self, call, data, form, inline):
        await self.formOrderAdvertiser_level8.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            text = await form.menu_last_preview(campaign_name=data.get("formOrder").get("campaign").get("name"))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=text, reply_markup=await inline.menu_last_preview(),
                                        disable_web_page_preview=True)

    # menu check post
    async def menu_check_post(self, call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as data:
            await self._send_post(call, data)
            if data.get("formOrder").get("campaign").get("media") is not None:
                await self._send_document(call, data)
            # await self._send_document(call, data)
            print(data.get('formOrder').get("campaign").get("media"))

    async def _send_post(self, call, data):
        Type = data.get("formOrder").get("campaign").get("post").get("type")
        Lang, reply, inline, form = await self._prepare_post(data)
        if Type == "photo":
            await self._send_post_photo(call, data, form, inline)
        elif Type == "video":
            await self._send_post_video(call, data, form, inline)
        elif Type == "text":
            await self._send_post_text(call, data, form, inline)

    async def _send_document(self, call, data):
        Type = data.get("formOrder").get("campaign").get("media", {}).get("type")
        if Type == "document":
            await self._send_media_document(call, data)
        elif Type == "photo":
            await self._send_media_photo(call, data)
        # if Type == "video":
        #     await self._send_media_video(call, data)

    @staticmethod
    async def _send_post_photo(call, data, form, inline):
        post = data.get("formOrder").get("campaign").get("post")
        text = await form.menu_post(caption=post.get("caption"),
                                    comment=data.get("formOrder").get("campaign").get("comment"))
        await bot.send_photo(chat_id=call.from_user.id, photo=post.get("file_id"), caption=text,
                             parse_mode="html", reply_markup=await inline.menu_check_post())

    @staticmethod
    async def _send_post_video(call, data, form, inline):
        post = data.get("formOrder").get("campaign").get("post")
        text = await form.menu_post(caption=post.get("caption"),
                                    comment=data.get("formOrder").get("campaign").get("comment"))
        await bot.send_video(chat_id=call.from_user.id, video=post.get("file_id"), caption=text,
                             parse_mode="html", reply_markup=await inline.menu_check_post())

    @staticmethod
    async def _send_post_text(call, data, form, inline):
        post = data.get("formOrder").get("campaign").get("post")
        text = await form.menu_post(caption=post.get("caption"),
                                    comment=data.get("formOrder").get("campaign").get("comment"))
        await bot.send_message(chat_id=call.from_user.id, text=text, parse_mode="html",
                               reply_markup=await inline.menu_check_post())

    @staticmethod
    async def _send_media_document(call, data):
        post = data.get("formOrder").get("campaign").get("media")
        await bot.send_document(chat_id=call.from_user.id, document=post.get("file_id"))

    @staticmethod
    async def _send_media_photo(call, data):
        post = data.get("formOrder").get("campaign").get("media")
        await bot.send_photo(chat_id=call.from_user.id, photo=post.get("file_id"))

    @staticmethod
    async def _send_media_video(call, data):
        post = data.get("formOrder").get("campaign").get("media")
        await bot.send_video(chat_id=call.from_user.id, video=post.get("file_id"))

    async def default(self, call: types.CallbackQuery, state: FSMContext):
        print(call.data)
        print(await state.get_state())

    def register_handlers_form_order(self, dp: Dispatcher):
        # dp.register_message_handler(self.menu_form_order, text=Txt.menu.formOrder,                                      state="MenuAdvertiser:menuAdvertiser_level1")
        # dp.register_callback_query_handler(self.menu_form_order, text="back",                                           state=self.formOrderAdvertiser_level2)
        # dp.register_callback_query_handler(self.menu_form_order, text=["back", "confirm"],                              state=[self.category_level1, self.parameters_level1, self.network_level1])
        #
        # dp.register_callback_query_handler(self.menu_category,  text='Category',                                        state=[self.formOrderAdvertiser_level1, self.search_filters_level1])
        # dp.register_callback_query_handler(self.menu_change_category, lambda x: x.data.startswith("category"),          state=[self.category_level1, self.category_level2])
        # dp.register_callback_query_handler(self.menu_category_turn, text=['next', 'prev'],                              state=[self.category_level1, self.category_level2])
        #
        # dp.register_callback_query_handler(self.menu_network, text='network',                                           state=self.formOrderAdvertiser_level1)
        # dp.register_callback_query_handler(self.menu_change_network, lambda x: x.data.startswith("kind"),              state=self.network_level1)

        # dp.register_callback_query_handler(self.menu_parameters, text='parameters',                                     state=[self.formOrderAdvertiser_level1])
        # dp.register_callback_query_handler(self.menu_parameters, text=['back', "confirm"],                              state=[self.lang_level1, self.sex_level1, self.age_level1, self.region_level1])
        #
        # dp.register_callback_query_handler(self.menu_parameters_from_search, text='parameters',                         state=[self.search_filters_level1])
        # dp.register_callback_query_handler(self.menu_parameters_from_search, text=['back', "confirm"],                  state=[self.lang_level2, self.sex_level2, self.age_level2, self.region_level2])
        #
        # dp.register_callback_query_handler(self.menu_lang, text='Lang',                                                 state=[self.parameters_level1, self.parameters_level2])
        # dp.register_callback_query_handler(self.menu_change_lang, lambda x: x.data.startswith("platformLang"),          state=[self.lang_level1, self.lang_level2])
        #
        # dp.register_callback_query_handler(self.menu_sex, text='Sex',                                                   state=[self.parameters_level1, self.parameters_level2])
        # dp.register_callback_query_handler(self.menu_get_sex, lambda x: x.data.startswith("sex"),                       state=[self.sex_level1, self.sex_level2])
        #
        # dp.register_callback_query_handler(self.menu_age, text='Age',                                                   state=[self.parameters_level1, self.parameters_level2])
        # dp.register_callback_query_handler(self.menu_change_age, lambda x: x.data.startswith("age"),                    state=[self.age_level1, self.age_level2])
        #
        # dp.register_callback_query_handler(self.menu_region, text='Region',                                             state=[self.parameters_level1, self.parameters_level2])
        # dp.register_callback_query_handler(self.menu_change_region, lambda x: x.data.startswith("region"),              state=[self.region_level1, self.region_level2])

        # dp.register_callback_query_handler(self.menu_all_platform, text="confirm",                                      state=[self.formOrderAdvertiser_level1, self.search_filters_level1])
        # dp.register_callback_query_handler(self.menu_all_platform, text="back",                                         state=[self.formOrderAdvertiser_level3, self.search_filters_level1, self.current_platform_level1])
        # dp.register_callback_query_handler(self.menu_all_platform_turn, text=["prev", "next"],                          state=self.formOrderAdvertiser_level2)
        # dp.register_callback_query_handler(self.menu_change_sorted, text=["subs_default",
        #                                                                   "subs_reverse",
        #                                                                   "price_default",
        #                                                                   "price_reverse"],                             state=self.formOrderAdvertiser_level2)
        # dp.register_callback_query_handler(self.menu_change_accommodation, lambda x: x.data.startswith("accommFilter"), state=self.formOrderAdvertiser_level2)
        # dp.register_callback_query_handler(self.menu_change_platform_type, lambda x: x.data.startswith("platformFilter"), state=self.formOrderAdvertiser_level2)

        # dp.register_callback_query_handler(self.menu_current_platform, lambda x: x.data.startswith("platform"),         state=self.formOrderAdvertiser_level2)
        # dp.register_callback_query_handler(self.menu_change_current_platform_accommodation,
        #                                    lambda x: x.data.startswith("accommodation"),                                state=self.current_platform_level1)

        # dp.register_callback_query_handler(self.menu_add_basket, text="addBasket",                                      state=self.current_platform_level1)
        #
        # dp.register_callback_query_handler(self.menu_search_filters, text="search",                                     state=self.formOrderAdvertiser_level2)
        # dp.register_callback_query_handler(self.menu_search_filters, text=["back", "confirm"],                          state=[self.find_level1, self.category_level2, self.parameters_level2])

        # dp.register_callback_query_handler(self.menu_search, text="find",                                               state=self.search_filters_level1)
        # dp.register_message_handler(self.menu_get_search, IsSearch(), content_types='text',                             state=self.find_level1)
        # dp.register_callback_query_handler(self.menu_delete_search, text="deleteSearch",                                state=self.formOrderAdvertiser_level2)
        #
        dp.register_message_handler(self.menu_basket, text=Txt.menu.basket,                                             state=self.formOrderAdvertiser_level2)
        dp.register_callback_query_handler(self.menu_basket, text="back",                                               state=self.formOrderAdvertiser_level4)
        dp.register_callback_query_handler(self.menu_delete_basket, lambda x: x.data.startswith("delete"),              state=self.formOrderAdvertiser_level3)

        dp.register_message_handler(self.menu_campaign, text=Txt.menu.task,                                             state=self.formOrderAdvertiser_level3)

        dp.register_message_handler(self.menu_campaign_web_app, content_types=["web_app_data"],                           state='*')

        dp.register_callback_query_handler(self.menu_campaign, text="back",                                             state=self.formOrderAdvertiser_level5)

        dp.register_message_handler(self.menu_name_campaign, content_types="text",                                      state=self.formOrderAdvertiser_level4)
        dp.register_callback_query_handler(self.menu_name_campaign, text="back",                                        state=self.formOrderAdvertiser_level6)

        dp.register_message_handler(self.menu_post, IsPostLength(), content_types=["photo", "video", "text"],           state=self.formOrderAdvertiser_level5)
        dp.register_callback_query_handler(self.menu_post, text="back",                                                 state=[self.url_level1, self.media_level1, self.comment_level1,
                                                                                                                               self.formOrderAdvertiser_level7])

        dp.register_callback_query_handler(self.menu_url, text="url",                                                   state=self.formOrderAdvertiser_level6)
        dp.register_callback_query_handler(self.menu_delete_url, text="deleteUrl",                                      state=self.formOrderAdvertiser_level6)
        dp.register_message_handler(self.menu_get_url, IsUrlButton(), content_types="text",                             state=self.url_level1)

        dp.register_callback_query_handler(self.menu_media_files, text="media",                                         state=self.formOrderAdvertiser_level6)
        dp.register_callback_query_handler(self.menu_delete_media_files, text="deleteMedia",                            state=self.formOrderAdvertiser_level6)
        dp.register_message_handler(self.menu_get_media, content_types=["photo", "video", "document"],                  state=self.media_level1)

        dp.register_callback_query_handler(self.menu_comment, text="comment",                                           state=self.formOrderAdvertiser_level6)
        dp.register_callback_query_handler(self.menu_delete_comment, text="deleteComment",                              state=self.formOrderAdvertiser_level6)
        dp.register_message_handler(self.menu_get_comment, IsCommentLength(), content_types="text",                     state=self.comment_level1)

        dp.register_message_handler(self.menu_all_dates, text=Txt.common.confirm,                                       state=self.formOrderAdvertiser_level6)
        dp.register_callback_query_handler(self.menu_all_dates, text="back",                                            state=[self.calendar_level1, self.formOrderAdvertiser_level8])

        dp.register_callback_query_handler(self.menu_calendar, lambda x: x.data.startswith("calendar"),                 state=self.formOrderAdvertiser_level7)
        dp.register_callback_query_handler(self.menu_calendar, text="back",                                             state=self.time_level_1)
        dp.register_callback_query_handler(self.menu_calendar_turn, text=['next', 'prev'],                              state=self.calendar_level1)
        dp.register_callback_query_handler(self.menu_calendar_busy, text="busyDate",                                    state=self.calendar_level1)

        dp.register_callback_query_handler(self.menu_time, lambda x: x.data.startswith("day"),                          state=self.calendar_level1)
        dp.register_callback_query_handler(self.menu_change_time, lambda x: x.data.startswith("time"),                  state=self.time_level_1)
        dp.register_callback_query_handler(self.menu_all_time, text="allTime",                                          state=self.time_level_1)

        dp.register_callback_query_handler(self.menu_get_day, text="confirm",                                           state=self.time_level_1)

        dp.register_callback_query_handler(self.menu_last_preview, text="confirm",                                      state=[self.formOrderAdvertiser_level7])
        dp.register_callback_query_handler(self.menu_last_preview, text="back",                                         state="FormOrderWallet:walletFormOrder_level1")

        dp.register_callback_query_handler(self.menu_check_post, text="checkPost",                                      state=self.formOrderAdvertiser_level8)

        # dp.register_callback_query_handler(self.default, lambda x: x.data.startswith(""),                                           state="*")

