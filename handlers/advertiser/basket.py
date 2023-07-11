from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from config import bot
from handlers.advertiser.form_order.form_order import FormOrderAdvertiser
from keyboards.inline.advertiser.form_order import InlineFormOrderAdvertiser
from keyboards.reply.advertiser.advertiser import ReplyAdvertiser
from looping import fastapi
from text.advertiser.formOrder import FormOrder
from text.fuction.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class BasketAdvertiser(StatesGroup):

    async def menu_basket(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await self._check_basket(message, data, state)

    async def _check_basket(self, message, data, state):
        status, Json = await fastapi.get_unpaid_basket(token=data.get("token"), language=data.get("lang"))
        if status == 200:
            await state.set_state("FormOrderAdvertiser:formOrderAdvertiser_level3")
            await self._unpack_basket(data, Json)
            Lang, reply, inline, form = await self._prepare_basket(data)
            await self._basket(message, inline, form, reply, Lang, data)
        elif status == 400:
            Lang = Txt.language[data.get('lang')]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.alert.advertiser.emptyBasket)

    @staticmethod
    async def _prepare_basket(data):
        Lang = Txt.language[data.get('lang')]
        reply = ReplyAdvertiser(language=data.get('lang'))
        inline = InlineFormOrderAdvertiser(language=data.get('lang'), token=data.get("token"),
                                           platform_list=data.get('formOrder').get("basket").get("channels"))
        form = FormOrder(data=data.get('formOrder').get("basket"), language=data.get("lang"))
        return Lang, reply, inline, form

    @staticmethod
    async def _basket(call, inline, form, reply, Lang, data):
        message2 = await bot.send_message(chat_id=call.from_user.id, text=Lang.menu.advertiser.formOrder,
                                          reply_markup=await reply.menu_task(login=data['email'], password=data['password']))
        message1 = await bot.send_message(chat_id=call.from_user.id, text=await form.menu_basket(),
                                          reply_markup=await inline.menu_basket(),
                                          disable_web_page_preview=True)
        data['message_id_None'] = message2.message_id
        data['message_id'] = message1.message_id

    async def _unpack_basket(self, data, Json):
        formOrder = FormOrderAdvertiser()
        await formOrder._callback_form_order(data)
        await formOrder._get_all_category(data)
        await formOrder._change_parameter(parameter=data.get("formOrder").get("category"), new_id="category_1")
        await self._get_unpaid_basket(data, Json)

    @staticmethod
    async def _get_unpaid_basket(data, Json):
        data.get('formOrder').get("basket")["channels"] = Json.get("channels")
        selected = []
        for channel in Json.get("channels"):
            selected.append(channel.get("id"))
        data.get('formOrder').get("siteRequest")["selected"] = selected

    def register_handlers_basket(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_basket, text=Txt.menu.basket,                                             state="MenuAdvertiser:menuAdvertiser_level1")
