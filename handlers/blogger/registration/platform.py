from contextlib import suppress
from random import randint
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound, MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted

from config import bot
from handlers.group.send_moderation import SendModeration
from keyboards.inline.common.personal_data import InlinePersonalData
from keyboards.inline.blogger.platform import InlinePlatformBlogger
from keyboards.reply.common.user import ReplyUser
from looping import fastapi, pg
from model.platform import Params, Values, Validate
from text.blogger.formPlatform import FormPlatform
from text.common.formPersonalData import FormPersonalData
from text.language.main import Text_main
from filters.platform import IsTitle, IsDescription, IsPrice, LenSymbol, IsInstagram
from text.fuction.decoding import Decoding
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FirstPlatformBlogger(StatesGroup):

    firstPlatform_level1 = State()
    firstPlatform_level2 = State()
    firstPlatform_level3 = State()
    firstPlatform_level4 = State()
    firstPlatform_level5 = State()
    firstPlatform_level6 = State()
    firstPlatform_level7 = State()
    firstPlatform_level8 = State()
    firstPlatform_level9 = State()
    firstPlatform_level10 = State()
    firstPlatform_level11 = State()
    firstPlatform_level12 = State()
    firstPlatform_level13 = State()
    firstPlatform_level14 = State()
    firstPlatform_level15 = State()

    price_level1 = State()

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

    # add platform
    async def menu_add(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state("RegistrationBlogger:regBlogger_level5")
        async with state.proxy() as data:
            reply, Lang, inline = await self._prepare(data)
            await self._add(call, Lang, inline)

    @staticmethod
    async def _add(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.registration.common.blogger,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_add())

    # Choose platform
    async def menu_kind(self, call: types.CallbackQuery, state: FSMContext):
        await self.firstPlatform_level1.set()
        async with state.proxy() as data:
            reply, Lang, inline = await self._prepare(data)
            await self._callback_kind(data)
            await self._kind(call, Lang, inline)
            print(data)

    @staticmethod
    async def _callback_kind(data):
        if data.get('area') is None:
            data["area"] = {}

    @staticmethod
    async def _kind(call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.add,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_kind())

    # platform Url
    async def menu_platform(self, call: types.CallbackQuery, state: FSMContext):
        await self.firstPlatform_level2.set()
        async with state.proxy() as data:
            reply, Lang, inline = await self._prepare(data)
            text = await self._check_platform_call(call, data, Lang)
            await self._platform(call, text, inline)

    @staticmethod
    async def _platform(call, text, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, reply_markup=await inline.menu_back(),
                                        text=text, message_id=call.message.message_id)

    async def _check_platform_call(self, call, data, Lang):
        await self._callback_platform(call, data)
        text = Lang.platform.blogger.dict[data.get("area").get("platform_id")]
        return text

    @staticmethod
    async def _callback_platform(call, data):
        dta = call.data.split("_")
        if dta[0] == "kind":
            data.get("area")["platform_id"] = int(dta[1])
            data.get("area")["platform"] = await Decoding(language=data.get("lang"), token=data.get("token"),
                                                          param_id=int(dta[1])).get_platform()
            data.get("area")["accommodation"] = {}

    # platform Title
    async def menu_title(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            reply, Lang, inline = await self._prepare(data)
            if isinstance(message, types.Message):
                await self._validate_platform(message, data, Lang, inline)
            elif isinstance(message, types.CallbackQuery):
                await self.firstPlatform_level3.set()
                await self._title_back(message, Lang, inline)

    async def _validate_platform(self, message, data, Lang, inline):
        json = Validate(type=data.get("area").get("platform_id"), url=message.text)
        status, json = await fastapi.validate_url(token=data.get("token"), json=json)
        form = FormPlatform(data=json, language=data.get("lang"))
        if status == 200:
            await self.firstPlatform_level3.set()
            await self._title(message, data, Lang, inline)
        elif json.get("error") == "already exist area":
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.blogger.platformExist)
        elif json.get("error") == "Restricted expire through":
            await bot.send_message(chat_id=message.from_user.id, text=await form.platform_reject())
        elif json.get("error") == "Banned":
            await bot.send_message(chat_id=message.from_user.id, text=await form.platform_ban())
        else:
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.common.nonFormat)

    @staticmethod
    async def _prepare(data):
        reply = ReplyUser(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), token=data.get("token"))
        return reply, Lang, inline

    async def _title(self, message, data, Lang, inline):
        data.get("area")['url'] = message.text
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.platform.blogger.title,
                                          reply_markup=await inline.menu_back())
        data['message_id'] = message1.message_id

    async def _title_back(self, message, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, text=Lang.platform.blogger.title,
                                        message_id=message.message.message_id, reply_markup=await inline.menu_back())

    # check valid url
    async def menu_verification(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        message = message
        await self.firstPlatform_level4.set()
        async with state.proxy() as data:
            reply, Lang, inline = await self._prepare(data)
            text, markup = await self._check_platform(data, Lang, inline)
            if isinstance(message, types.Message):
                await self._check_verification(message, data, text, markup)
            elif isinstance(message, types.CallbackQuery):
                await self._check_verification_back(message, data, text, markup)

    async def _check_platform(self, data, Lang, inline):
        form = FormPlatform(language=data.get('lang'))
        data["code"] = data.get("code") if data.get("code") is not None else randint(100000, 999999)
        text = await form.menu_telegram_verification(code=data.get("code"))
        markup = await inline.menu_telegram()
        return text, markup

    async def _check_verification(self, message, data, text, markup):
        data.get("area")['name'] = message.text
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
        data['message_id'] = message1.message_id

    async def _check_verification_back(self, message, data, text, markup):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, text=text, message_id=message.message.message_id,
                                        reply_markup=markup)

    # choose category of platform
    async def menu_category(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            if message.data == "check":
                await self._check_verify(message, data)
            elif message.data == "back":
                Lang, inline = await self._prepare_category(data)
                await self._category(message, Lang, inline)

    async def _check_verify(self, message, data):
        json = Validate(type=data.get("area").get("platform_id"), url=data.get("area").get("url"),
                        code=data.get("code"))
        status = await fastapi.verify_channel(json=json, token=data.get("token"))
        Lang = Txt.language[data.get('lang')]
        status = 200
        if status == 200:
            await message.answer(show_alert=True, text=Lang.alert.blogger.telegram_success)
            await self._get_all_category(data)
            Lang, inline = await self._prepare_category(data)
            await self._category(message, Lang, inline)
        else:
            await message.answer(show_alert=True, text=Lang.alert.blogger.telegram_error)

    @staticmethod
    async def _prepare_category(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), page=data.get("area").get("category").get("page"),
                                       category=data.get("area").get("category"))
        return Lang, inline

    @staticmethod
    async def _get_all_category(data):
        if data.get("area").get("category") is None:
            params = Params(language=data.get('lang'), offset=0, limit=100)
            all_category = await fastapi.get_channel_categories(params=params, token=data.get('token'))
            max_page = await func.max_page(units=all_category["types"])
            data.get("area")["category"] = Values(all_values=all_category["types"], page=1, max_page=max_page)

    async def _category(self, message, Lang, inline):
        await self.firstPlatform_level5.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                        text=Lang.platform.blogger.category, reply_markup=await inline.menu_category())

    # menu turn page category
    async def menu_category_turn(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._callback_category(call, data)
            Lang, inline = await self._prepare_category(data)
            await self._category_turn(call, Lang, inline)

    async def _category_turn(self, call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Lang.platform.blogger.category, reply_markup=await inline.menu_category())

    async def _callback_category(self, call, data):
        page = data.get("area").get("category").get("page")
        if call.data == "next" and page < data.get("area").get("category").get("max_page"):
            data.get("area").get("category")["page"] += 1
        elif call.data == "prev" and page > 1:
            data.get("area").get("category")["page"] -= 1

    # choose languages of platform
    async def menu_lang(self, call: types.CallbackQuery, state: FSMContext):
        await self.firstPlatform_level6.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare_lang(data)
            await self._lang(call, Lang, inline)
            await self._callback_lang(call, data)
            print(data)

    async def _callback_lang(self, call, data):
        dta = call.data.split("_")
        if dta[0] == "category":
            data.get("area")["category"]["id"] = int(dta[1])
            data.get("area")["category"]["value"] = \
                await self._get_value2(parameter_id=int(dta[1]),
                                       values=data.get("area").get("category").get("all_values"))

    async def _prepare_lang(self, data):
        await self._get_all_lang(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), platform_lang=data.get("area").get("platformLang"))
        return Lang, inline

    async def _get_all_lang(self, data):
        if data.get("area").get("platformLang") is None:
            params = Params(language=data.get('lang'), offset=0, limit=40)
            all_platformLang = await fastapi.get_channel_languages(params=params, token=data.get('token'))
            data.get("area")["platformLang"] = Values(all_values=all_platformLang["types"], id=[], values=[])

    async def _lang(self, call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.lang,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_lang())

    # change languages of platform
    async def menu_change_lang(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("area").get("platformLang"), new_id=call.data)
            Lang, inline = await self._prepare_lang(data)
            await self._lang(call, Lang, inline)

    # choose regions of platform
    async def menu_region(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_lang(call, data)
            print(data)

    async def _prepare_region(self, data):
        await self._get_all_regions(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), regions=data.get("area").get("regions"),
                                       token=data.get("token"))
        return Lang, inline

    async def _get_all_regions(self, data):
        if data.get("area").get("regions") is None:
            params = Params(language=data.get('lang'), offset=0, limit=40)
            all_regions = await fastapi.get_regions(params=params, token=data.get('token'))
            data.get("area")["regions"] = Values(all_values=all_regions["types"], id=[], values=[])

    # checking count of languages
    async def _check_lang(self, call, data):
        Lang, inline = await self._prepare_region(data)
        if len(data.get("area").get("platformLang").get("id")) == 0:
            await call.answer(text=Lang.alert.blogger.lang, show_alert=True)
        else:
            await self._region(call, Lang, inline)

    async def _region(self, call, Lang, inline):
        await self.firstPlatform_level7.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.region,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_region())

    # change regions of platform
    async def menu_change_region(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("area").get("regions"), new_id=call.data)
            Lang, inline = await self._prepare_region(data)
            await self._region(call, Lang, inline)
            print(data)

    # platform description
    async def menu_description(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_region(call, data)
            print(data)

    # checking count of regions
    async def _check_region(self, call, data):
        reply, Lang, inline = await self._prepare(data)
        if len(data.get("area").get("regions").get("id")) == 0:
            await call.answer(text=Lang.alert.blogger.region, show_alert=True)
        else:
            await self._description(call, Lang, inline)

    async def _description(self, call, Lang, inline):
        await self.firstPlatform_level8.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.description,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_back())

    # choose sex of platform
    async def menu_sex(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.firstPlatform_level9.set()
        async with state.proxy() as data:
            reply, Lang, inline = await self._prepare(data)
            if isinstance(message, types.Message):
                await self._sex(message, data, Lang, inline)
            elif isinstance(message, types.CallbackQuery):
                await self._sex_back(message, Lang, inline)

    async def _sex(self, message, data, Lang, inline):
        data.get("area")['description'] = message.text
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))
        message1 = await bot.send_message(chat_id=message.from_user.id, text=Lang.platform.blogger.sex,
                                          reply_markup=await inline.menu_sex())
        data['message_id'] = message1.message_id

    async def _sex_back(self, message, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                        text=Lang.platform.blogger.sex, reply_markup=await inline.menu_sex())

    # choose age of platform
    async def menu_age(self, call: types.CallbackQuery, state: FSMContext):
        await self.firstPlatform_level10.set()
        async with state.proxy() as data:
            Lang, inline = await self._prepare_age(data)
            await self._age(call, Lang, inline)
            await self._callback_age(call, data)

    async def _prepare_age(self, data):
        await self._get_all_ages(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), age=data.get("area").get("age"))
        return Lang, inline

    async def _get_all_ages(self, data):
        if data.get("area").get("age") is None:
            params = Params(language=data.get('lang'))
            all_ages = await fastapi.get_channel_age_ratios(params=params, token=data.get('token'))
            data.get("area")["age"] = Values(all_values=all_ages["types"], id=[], values=[])

    async def _age(self, call, Lang, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.platform.blogger.age,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_age())

    async def _callback_age(self, call, data):
        dta = call.data.split("_")
        if dta[0] == "sex":
            data.get("area")["sex"] = int(dta[1])
            data.get("area")["sex_value"] = await Decoding(language=data.get("lang"), token=data.get("token"),
                                                           param_id=data.get("area").get("sex")).get_sex()

    # change age of platform
    async def menu_change_age(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._change_parameter(parameter=data.get("area").get("age"), new_id=call.data)
            Lang, inline = await self._prepare_age(data)
            await self._age(call, Lang, inline)

    # choose format of platform
    async def menu_format(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            if isinstance(message, types.CallbackQuery):
                await self._format_call(message, data)
            elif isinstance(message, types.Message):
                await self._price_get(message, data)
            print(data)

    async def _format_call(self, message, data):
        if message.data == "confirm":
            await self._check_age(message, data)
        elif message.data == "clean":
            for accommodation in data.get('area').get("accommodation"):
                accommodation.update({"price": None})
            await self._format(message, data)
        elif message.data == "back":
            await self._format_back(message, data)

    async def _prepare_format(self, data):
        await self._get_all_formats(data)
        Lang = Txt.language[data.get('lang')]
        inline = InlinePlatformBlogger(language=data.get('lang'), formats=data.get("area").get("accommodation"))
        reply = ReplyUser(language=data.get('lang'))
        form = FormPlatform(language=data.get('lang'), data=data.get('area').get("accommodation"))
        return Lang, inline, reply, form

    # check count of ages
    async def _check_age(self, message, data):
        if len(data.get("area").get("age", {}).get("id", [])) == 0:
            Lang = Txt.language[data.get('lang')]
            await message.answer(text=Lang.alert.blogger.age, show_alert=True)
        else:
            await self._format(message, data)

    async def _get_all_formats(self, data):
        if len(data.get("area").get("accommodation")) == 0:
            params = Params(language=data.get('lang'), channel_type=data.get("area").get('platform_id'))
            json = await fastapi.get_channel_accommodations(params=params, token=data.get('token'))
            all_formats = json.get("types")
            for accommodation in all_formats:
                accommodation.update({"price": None})
            data.get('area')["accommodation"] = all_formats

    async def _format(self, message, data):
        Lang, inline, reply, form = await self._prepare_format(data)
        await self.firstPlatform_level11.set()
        with suppress(MessageNotModified, MessageToEditNotFound):
            await message.answer()
            await bot.edit_message_text(chat_id=message.from_user.id, text=await form.menu_formats(),
                                        reply_markup=await inline.menu_format(), message_id=message.message.message_id)

    async def _format_back(self, message, data):
        Lang, inline, reply, form = await self._prepare_format(data)
        await self.firstPlatform_level11.set()
        message_2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.platform,
                                           reply_markup=await reply.main_menu())
        await self._delete_message(message, data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_formats(),
                                          reply_markup=await inline.menu_format())
        data['message_id_None'] = message_2.message_id
        data['message_id'] = message1.message_id

    async def _delete_message(self, message, data):
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id_None'))
        with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
            await bot.delete_message(chat_id=message.from_user.id, message_id=data.get('message_id'))

    async def _price_get(self, message, data):
        current_format = data.get("area")["current_format"]
        for accommodation in data.get('area').get("accommodation"):
            if int(current_format) == int(accommodation.get("id")):
                accommodation.update({"price": int(message.text)})
        await self._format_back(message, data)

    # platform price of current format
    async def menu_price(self, call: types.CallbackQuery, state: FSMContext):
        await self.price_level1.set()
        async with state.proxy() as data:
            formats = call.data.split("_")[1]
            data.get("area")["current_format"] = formats
            inline = InlinePlatformBlogger(language=data.get('lang'))
            form = FormPlatform(data=data.get("area").get('accommodation'),
                                formats=data.get("area").get('current_format'), language=data.get('lang'))
            with suppress(MessageNotModified, MessageToEditNotFound):
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_price(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_back())
            print(data)

    # platform symbol limit
    async def menu_symbol(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await self._check_price(call, data)
            print(data)

        # check count of price&format

    async def _check_price(self, call, data):
        reply, Lang, inline = await self._prepare(data)
        for accommodation in data.get("area").get("accommodation"):
            if accommodation.get('price') is not None:
                await self._symbol(call, data, Lang, inline)
                break
        else:
            await call.answer(text=Lang.alert.blogger.price, show_alert=True)

    async def _symbol(self, call, data, Lang, inline):
        await self.firstPlatform_level12.set()
        reply = ReplyUser(language=data.get('lang'))
        message_2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.blogger.platform,
                                           reply_markup=await reply.menu_skip())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=Lang.platform.blogger.symbol,
                                          reply_markup=await inline.menu_back())
        data['message_id_None'] = message_2.message_id
        data['message_id'] = message1.message_id

    # platform Main Form
    async def menu_check_platform(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.firstPlatform_level13.set()
        async with state.proxy() as data:
            if message.text.isnumeric() is True:
                data.get("area")["symbol"] = message.text
            else:
                data.get("area")["symbol"] = None
            inline, Lang, form, reply = await self._prepare_check_platform(data)
            await self._main_platform(message, data, Lang, form, inline, reply)
            print(data)

    @staticmethod
    async def _prepare_check_platform(data):
        inline = InlinePlatformBlogger(language=data.get('lang'))
        Lang = Txt.language[data.get('lang')]
        form = FormPlatform(data=data.get("area"), language=data.get('lang'))
        reply = ReplyUser(language=data.get('lang'))
        return inline, Lang, form, reply

    async def _main_platform(self, message, data, Lang, form, inline, reply):
        message2 = await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.platform,
                                          reply_markup=await reply.main_menu())
        await self._delete_message(message, data)
        message1 = await bot.send_message(chat_id=message.from_user.id, text=await form.menu_platform(),
                                          reply_markup=await inline.menu_check(), disable_web_page_preview=True)
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id
        
    # end of adding platform & starting create blogger
    async def menu_end(self, call: types.CallbackQuery, state: FSMContext):
        await self.firstPlatform_level14.set()
        async with state.proxy() as data:
            await self._end_check(call, data)

    async def _end_check(self, call, data):
        Lang, inline, form_platform, reply = await self._prepare_end(data)
        await self._end(call, data, Lang, form_platform, inline, reply)
        await self._send_group(call, data)
        data.pop("area")

    @staticmethod
    async def _send_group(call, data):
        send_group = SendModeration(data=data, user_id=call.from_user.id)
        await send_group.send_group()

    @staticmethod
    async def _prepare_end(data):
        Lang = Txt.language[data.get('lang')]
        inline = InlinePersonalData(language=data.get('lang'))
        form_platform = FormPersonalData(data=data)
        reply = ReplyUser(language=data.get('lang'))
        return Lang, inline, form_platform, reply

    async def _end(self, call, data, Lang, form_platform, inline, reply):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.platform.blogger.end,
                                          reply_markup=await reply.menu_next_time())
        await self._delete_message(call, data)
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form_platform.menu_start(),
                                          reply_markup=await inline.menu_add_data())
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    async def menu_add_data(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.firstPlatform_level15.set()
        async with state.proxy() as data:
            Lang, inline, form_platform, reply = await self._prepare_end(data)
            await self._add_data(message, form_platform, inline)

    @staticmethod
    async def _add_data(call, form_platform, inline):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form_platform.menu_personal_data(),
                                        reply_markup=await inline.menu_employment())

    def register_handlers_first_platform(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_add, text="back",                                                  state=self.firstPlatform_level1)

        dp.register_callback_query_handler(self.menu_kind, text="add",                                                  state="RegistrationBlogger:regBlogger_level5")
        dp.register_callback_query_handler(self.menu_kind, text="back",                                                 state=self.firstPlatform_level2)

        dp.register_callback_query_handler(self.menu_platform, IsInstagram(), lambda x: x.data.startswith("kind"),      state=self.firstPlatform_level1)
        dp.register_callback_query_handler(self.menu_platform, text="back",                                             state=self.firstPlatform_level3)

        dp.register_message_handler(self.menu_title,               content_types='text',                                state=self.firstPlatform_level2)
        dp.register_callback_query_handler(self.menu_title, text='back',                                                state=self.firstPlatform_level4)

        dp.register_message_handler(self.menu_verification, IsTitle(), content_types='text',                            state=self.firstPlatform_level3)
        dp.register_callback_query_handler(self.menu_verification, text='back',                                         state=self.firstPlatform_level5)

        dp.register_callback_query_handler(self.menu_category,  text='check',                                           state=self.firstPlatform_level4)
        dp.register_callback_query_handler(self.menu_category,  text='authorization',                                   state=self.firstPlatform_level4)
        dp.register_callback_query_handler(self.menu_category_turn, text=['next', 'prev'],                              state=self.firstPlatform_level5)
        dp.register_callback_query_handler(self.menu_category, text='back',                                             state=self.firstPlatform_level6)

        dp.register_callback_query_handler(self.menu_lang, lambda x: x.data.startswith("category"),                     state=self.firstPlatform_level5)
        dp.register_callback_query_handler(self.menu_lang, text='back',                                                 state=self.firstPlatform_level7)
        dp.register_callback_query_handler(self.menu_change_lang, lambda x: x.data.startswith("platformLang"),          state=self.firstPlatform_level6)

        dp.register_callback_query_handler(self.menu_region, text="confirm",                                            state=self.firstPlatform_level6)
        dp.register_callback_query_handler(self.menu_region, text='back',                                               state=self.firstPlatform_level8)
        dp.register_callback_query_handler(self.menu_change_region, lambda x: x.data.startswith("region"),              state=self.firstPlatform_level7)

        dp.register_callback_query_handler(self.menu_description, text="confirm",                                       state=self.firstPlatform_level7)
        dp.register_callback_query_handler(self.menu_description, text='back',                                          state=self.firstPlatform_level9)

        dp.register_message_handler(self.menu_sex, IsDescription(), content_types='text',                               state=self.firstPlatform_level8)
        dp.register_callback_query_handler(self.menu_sex, text='back',                                                  state=self.firstPlatform_level10)

        dp.register_callback_query_handler(self.menu_age, lambda x: x.data.startswith("sex"),                           state=self.firstPlatform_level9)
        dp.register_callback_query_handler(self.menu_age, text='back',                                                  state=self.firstPlatform_level11)
        dp.register_callback_query_handler(self.menu_change_age, lambda x: x.data.startswith("age"),                    state=self.firstPlatform_level10)

        dp.register_callback_query_handler(self.menu_format, text="confirm",                                            state=self.firstPlatform_level10)
        dp.register_callback_query_handler(self.menu_format, text="back",                                               state=[self.price_level1, self.firstPlatform_level12])
        dp.register_callback_query_handler(self.menu_format, text="clean",                                              state=self.firstPlatform_level11)
        dp.register_message_handler(self.menu_format, IsPrice(), content_types='text',                                  state=self.price_level1)

        dp.register_callback_query_handler(self.menu_price, lambda x: x.data.startswith("format"),                      state=self.firstPlatform_level11)

        dp.register_callback_query_handler(self.menu_symbol, text="confirm",                                            state=self.firstPlatform_level11)
        dp.register_callback_query_handler(self.menu_symbol, text="back",                                               state=self.firstPlatform_level13)

        dp.register_message_handler(self.menu_check_platform, text=Txt.common.skip,                                     state=self.firstPlatform_level12)
        dp.register_message_handler(self.menu_check_platform, LenSymbol(), content_types='text',                        state=self.firstPlatform_level12)

        dp.register_callback_query_handler(self.menu_end, text="alright",                                               state=self.firstPlatform_level13)

        dp.register_callback_query_handler(self.menu_add_data, text="addData",                                          state=self.firstPlatform_level14)
        dp.register_callback_query_handler(self.menu_add_data, text="back",                                             state=["FirstSelfEmployedBlogger:firstData_level1", "FirstEntityBlogger:firstData_level1"])


