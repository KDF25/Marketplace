from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import *

from config import bot
from filters.platform import IsDescription, IsPrice
from keyboards.inline.blogger.platform import InlinePlatformBlogger
from looping import fastapi
from model.platform import UpdatePlatform, Params, Values
from text.blogger.formPlatform import FormPlatform
from text.fuction.decoding import Decoding
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class ChangePlatformBlogger(StatesGroup):

    changePlatform_level1 = State()
    changePlatform_level2 = State()

    title_level1 = State()
    description_level1 = State()
    lang_level1 = State()
    region_level1 = State()
    sex_level1 = State()
    age_level1 = State()
    format_level1 = State()
    price_level1 = State()

    @staticmethod
    async def _get_value(parameter_id: int, values: list):
        return values[parameter_id-1]["name"]

    @staticmethod
    async def _get_value2(parameter_id: int, values: list):
        Dict = {}
        for i in values:
            Dict[i['id']] = i["name"]
        return Dict[parameter_id]

    # change Languages, regions, ages
    async def _change_parameter(self, parameter: dict, new_id: str):
        list_id = parameter.get("id")
        list_values = parameter.get("values")
        new_id = int(new_id.split("_")[1])
        new_value = await self._get_value2(parameter_id=new_id, values=parameter.get("all_values"))
        if new_id not in list_id:
            list_id.append(new_id)
            list_values.append(new_value)
        elif new_id in list_id:
            list_id.remove(new_id)
            list_values.remove(new_value)

    async def menu_change(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_price2(call, data)

    async def _check_price2(self, call, data):
        inline, form = await self._prepare_change(data)
        for accommodation in data.get("current_platform").get("accommodation"):
            if accommodation.get('price') is not None:
                await self.changePlatform_level1.set()
                await self._change(call, form, inline)
                break
        else:
            Lang: Model = Txt.language[data.get('lang')]
            await call.answer(text=Lang.alert.blogger.price, show_alert=True)

    async def menu_change_back(self, call: types.CallbackQuery, state: FSMContext):
        await self.changePlatform_level1.set()
        async with state.proxy() as data:
            inline, form = await self._prepare_change(data)
            await self._change_back(call, data, form, inline)

    @staticmethod
    async def _prepare_change(data):
        inline = InlinePlatformBlogger(language=data.get('lang'))
        form = FormPlatform(data=data.get("current_platform"), language=data.get("lang"))
        return inline, form

    @staticmethod
    async def _change(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_change(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_change(),
                                        disable_web_page_preview=True)

    @staticmethod
    async def _change_back(call, data, form, inline):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=call.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form.menu_change(),
                                          reply_markup=await inline.menu_change(), disable_web_page_preview=True)
        data['message_id'] = message1.message_id

    @staticmethod
    async def _prepare(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), token=data.get("token"))
        return Lang, inline

    async def menu_description(self, call: types.CallbackQuery, state: FSMContext):
        await self.description_level1.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare(data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.change.description,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    async def menu_get_description(self, message: types.Message, state: FSMContext):
        await self.changePlatform_level1.set()
        async with state.proxy() as data:
            data.get("current_platform")['description'] = message.text
            inline, form = await self._prepare_change(data)
            await self._change_back(message, data, form, inline)
            await self._update_description(data)

    @staticmethod
    async def _update_description(data):
        params = UpdatePlatform(area_id=data.get("current_platform").get("id"),
                                description=data.get("current_platform").get('description'))
        await fastapi.update_description(params=params, token=data.get("token"))

    async def menu_parameters(self,  call: types.CallbackQuery, state: FSMContext):
        await self.changePlatform_level2.set()
        async with state.proxy() as data:
            inline, form = await self._prepare_change(data)
            await self._parameters(call, form, inline)

    @staticmethod
    async def _parameters(call, form, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_parameters(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_parameters())

    async def menu_lang(self, call: types.CallbackQuery, state: FSMContext):
        await self.lang_level1.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare_lang(data)
            await self._lang(call, Lang, inline)
            print(data)

    async def menu_change_lang(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("current_platform").get("platformLang"),
                                         new_id=call.data)
            Lang, inline = await self._prepare_lang(data)
            await self._lang(call, Lang, inline)

    async def _prepare_lang(self, data):
        await self._get_all_lang(data)
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'),  token=data.get("token"),
                                       platform_lang=data.get("current_platform").get("platformLang"))
        return Lang, inline

    @staticmethod
    async def _get_all_lang(data):
        if data.get("current_platform").get("platformLang").get("all_values") is None:
            params = Params(language=data.get('lang'), offset=0, limit=40)
            all_platformLang = await fastapi.get_channel_languages(params=params, token=data.get('token'))
            data.get("current_platform")["platformLang"].update(Values(all_values=all_platformLang["types"]))

    @staticmethod
    async def _lang(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.lang,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_lang())

    async def menu_get_lang(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_lang(call, data)

    @staticmethod
    async def _prepare_update(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'))
        form = FormPlatform(data=data.get("current_platform"), language=data.get("lang"))
        return Lang, inline, form

    async def _check_lang(self, call, data):
        Lang, inline, form = await self._prepare_update(data)
        if len(data.get("current_platform").get("platformLang").get("id")) == 0:
            await call.answer(text=Lang.alert.blogger.lang, show_alert=True)
        else:
            await self._parameters_update(call, Lang, form, inline)
            await self._update_languages(data)

    @staticmethod
    async def _update_languages(data):
        params = UpdatePlatform(area_id=data.get("current_platform").get("id"),
                                languages=data.get("current_platform").get("platformLang").get("id"))
        await fastapi.update_languages(params=params, token=data.get("token"))

    async def _parameters_update(self, call, Lang, form, inline):
        await self.changePlatform_level2.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer(text=Lang.alert.blogger.success, show_alert=True)
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_parameters(),
                                        message_id=call.message.message_id, reply_markup=await inline.menu_parameters())

    async def menu_region(self, call: types.CallbackQuery, state: FSMContext):
        await self.region_level1.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare_region(data)
            await self._region(call, Lang, inline)

    async def menu_change_region(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("current_platform").get("regions"), new_id=call.data)
            Lang, inline = await self._prepare_region(data)
            await self._region(call, Lang, inline)

    async def _prepare_region(self, data):
        await self._get_all_regions(data)
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), regions=data.get("current_platform").get("regions"))
        return Lang, inline

    @staticmethod
    async def _get_all_regions(data):
        if data.get("current_platform").get("regions").get("all_values") is None:
            params = Params(language=data.get('lang'), offset=0, limit=40)
            all_regions = await fastapi.get_regions(params=params, token=data.get('token'))
            data.get("current_platform")["regions"].update(Values(all_values=all_regions["types"]))

    @staticmethod
    async def _region(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.region,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_region())

    async def menu_get_region(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_region(call, data)

    async def _check_region(self, call, data):
        Lang, inline, form = await self._prepare_update(data)
        if len(data.get("current_platform").get("regions").get("id")) == 0:
            await call.answer(text=Lang.alert.blogger.region, show_alert=True)
        else:
            await self._parameters_update(call, Lang, form, inline)
            await self._update_regions(data)

    @staticmethod
    async def _update_regions(data):
        params = UpdatePlatform(area_id=data.get("current_platform").get("id"),
                                regions=data.get("current_platform").get("regions").get("id"))
        await fastapi.update_regions(params=params, token=data.get("token"))

    async def menu_sex(self, call:  types.CallbackQuery, state: FSMContext):
        await self.sex_level1.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare(data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.platform.blogger.sex, reply_markup=await inline.menu_sex())

    async def menu_get_sex(self, call: types.CallbackQuery, state: FSMContext):
        await self.changePlatform_level2.set()
        async with state.proxy() as data:
            await self._callback_sex(call, data)
            Lang, inline, form = await self._prepare_update(data)
            await self._parameters_update(call, Lang, form, inline)

    @staticmethod
    async def _callback_sex(call, data):
        data.get('current_platform')["sex"] = int(call.data.split("_")[1])
        data.get("current_platform")["sex_value"] = \
            await Decoding(language=data.get("lang"), token=data.get("token"),
                           param_id=data.get("current_platform").get("sex")).get_sex()

    async def menu_age(self, call: types.CallbackQuery, state: FSMContext):
        await self.age_level1.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare_age(data)
            await self._age(call, Lang, inline)

    async def _prepare_age(self, data):
        await self._get_all_ages(data)
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), age=data.get("current_platform").get("age"))
        return Lang, inline

    async def _get_all_ages(self, data):
        if data.get("current_platform").get("age").get("all_values") is None:
            params = Params(language=data.get('lang'))
            all_ages = await fastapi.get_channel_age_ratios(params=params, token=data.get('token'))
            data.get("current_platform")["age"].update(Values(all_values=all_ages["types"]))

    async def menu_change_age(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("current_platform").get("age"), new_id=call.data)
            Lang, inline = await self._prepare_age(data)
            await self._age(call, Lang, inline)

    @staticmethod
    async def _age(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.age,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_age())

    async def menu_get_age(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_age(call, data)

    async def _check_age(self, call, data):
        Lang, inline, form = await self._prepare_update(data)
        if len(data.get("current_platform").get("age").get("id")) == 0:
            await call.answer(text=Lang.alert.blogger.age, show_alert=True)
        else:
            await self._parameters_update(call, Lang, form, inline)
            await self._update_ages(data)

    @staticmethod
    async def _update_ages(data):
        params = UpdatePlatform(area_id=data.get("current_platform").get("id"),
                                ages=data.get("current_platform").get("age").get("id"))
        await fastapi.update_ages(params=params, token=data.get("token"))

    async def menu_format(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.format_level1.set()
        async with state.proxy() as data:
            if isinstance(message, types.CallbackQuery):
                await self._format_call(message, data)
            elif isinstance(message, types.Message):
                await self._price_get(message, data)
            print(data)

    async def _format_call(self, message, data):
        dta = message.data.split("_")
        if dta[0] == "price":
            await self._format(message, data)
        elif dta[0] == "clean":
            print(data.get("current_platform"))
            params = Params(language=data.get('lang'), channel_type=data.get("current_platform").get('platform_id'))
            json = await fastapi.get_channel_accommodations(params=params, token=data.get('token'))
            all_formats = json.get("types")
            for accommodation in all_formats:
                accommodation.update({"price": None})
            data.get('current_platform')["accommodation"] = all_formats
            await self._format(message, data)
        elif dta[0] == "back":
            await self._format_back(message, data)

    @staticmethod
    async def _prepare_format(data):
        Lang: Model = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), formats=data.get("current_platform").get("accommodation"))
        form = FormPlatform(language=data.get('lang'), data=data.get('current_platform').get("accommodation"))
        return Lang, inline, form

    async def _format(self, message, data):
        Lang, inline, form = await self._prepare_format(data)
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, text=await form.menu_formats(),
                                        reply_markup=await inline.menu_format(), message_id=message.message.message_id)

    async def _format_back(self, message, data):
        Lang, inline, form = await self._prepare_format(data)
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_formats(),
                                          reply_markup=await inline.menu_format())
        data['message_id'] = message1.message_id

    async def _price_get(self, message, data):
        current_format = data.get("current_platform")["current_format"]
        for accommodation in data.get('current_platform').get("accommodation"):
            if int(current_format) == int(accommodation.get("id")):
                accommodation.update({"price": int(message.text)})
        await self._format_back(message, data)

    async def menu_price(self, call: types.CallbackQuery, state: FSMContext):
        await self.price_level1.set()
        async with state.proxy() as data:
            formats = call.data.split("_")[1]
            data.get('current_platform')["current_format"] = formats
            inline = InlinePlatformBlogger(language=data.get('lang'))
            form = FormPlatform(data=data.get("current_platform").get('accommodation'),
                                formats=data.get('current_platform').get('current_format'), language=data.get('lang'))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_price(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_back())
            print(data)

    async def menu_get_price(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_price(call, data)

    async def _check_price(self, call, data):
        Lang, inline, form = await self._prepare_update(data)
        for accommodation in data.get("current_platform").get("accommodation"):
            if accommodation.get('price') is not None:
                await self.changePlatform_level1.set()
                await self._change(call, form, inline)
                await self._update_accommodations(data)
                break
        else:
            await call.answer(text=Lang.alert.blogger.price, show_alert=True)

    @staticmethod
    async def _update_accommodations(data):
        new_list = []
        for accommodation in data.get("current_platform").get("accommodation"):
            if accommodation['price'] is not None:
                new_list.append({"accommodation": accommodation['id'], "price": accommodation['price']})
        params = UpdatePlatform(area_id=data.get("current_platform").get("id"), accommodations=new_list)
        await fastapi.update_accommodations(params=params, token=data.get("token"))

    def register_handlers_change_platform_blogger(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_change, text="change",                                             state="PlatformBlogger:platform_level1")
        dp.register_callback_query_handler(self.menu_change, text="back",                                               state=[self.changePlatform_level2,  self.format_level1])
        dp.register_callback_query_handler(self.menu_change_back, text="back",                                          state=[self.title_level1, self.description_level1])

        dp.register_callback_query_handler(self.menu_description, text='description',                                   state=self.changePlatform_level1)

        dp.register_message_handler(self.menu_get_description, IsDescription(), content_types='text',                   state=self.description_level1)

        dp.register_callback_query_handler(self.menu_parameters, text='parameters',                                     state=self.changePlatform_level1)
        dp.register_callback_query_handler(self.menu_parameters, text='back',                                           state=[self.lang_level1,
                                                                                                                               self.sex_level1,
                                                                                                                               self.age_level1,
                                                                                                                               self.region_level1])

        dp.register_callback_query_handler(self.menu_lang, text='Lang',                                                 state=self.changePlatform_level2)
        dp.register_callback_query_handler(self.menu_change_lang, lambda x: x.data.startswith("platformLang"),          state=self.lang_level1)

        dp.register_callback_query_handler(self.menu_sex, text='Sex',                                                   state=self.changePlatform_level2)

        dp.register_callback_query_handler(self.menu_age, text='Age',                                                   state=self.changePlatform_level2)
        dp.register_callback_query_handler(self.menu_change_age, lambda x: x.data.startswith("age"),                    state=self.age_level1)

        dp.register_callback_query_handler(self.menu_region, text='Region',                                             state=self.changePlatform_level2)
        dp.register_callback_query_handler(self.menu_change_region, lambda x: x.data.startswith("region"),              state=self.region_level1)

        dp.register_callback_query_handler(self.menu_get_lang, text='confirm',                                          state=self.lang_level1)
        dp.register_callback_query_handler(self.menu_get_sex, lambda x: x.data.startswith("sex"),                       state=self.sex_level1)
        dp.register_callback_query_handler(self.menu_get_age, text='confirm',                                           state=self.age_level1)
        dp.register_callback_query_handler(self.menu_get_region, text='confirm',                                        state=self.region_level1)

        dp.register_callback_query_handler(self.menu_format, text='price',                                              state=self.changePlatform_level1)
        dp.register_callback_query_handler(self.menu_format, text="back",                                               state=self.price_level1)
        dp.register_callback_query_handler(self.menu_format, text="clean",                                              state=self.format_level1)
        dp.register_message_handler(self.menu_format, IsPrice(), content_types='text',                                  state=self.price_level1)

        dp.register_callback_query_handler(self.menu_price, lambda x: x.data.startswith("format"),                      state=self.format_level1)

        dp.register_callback_query_handler(self.menu_get_price, text='confirm',                                         state=self.format_level1)


