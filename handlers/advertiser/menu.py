from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from handlers.advertiser.all_orders.all_orders import AllOrderAdvertiser
from handlers.advertiser.form_order.form_order import FormOrderAdvertiser
from handlers.advertiser.form_order.payment_common import FormOrderPaymentCommon
from handlers.advertiser.form_order.payment_entity import FormOrderPaymentEntity
from handlers.advertiser.form_order.payment_individual import FormOrderPaymentIndividual
from handlers.advertiser.form_order.payment_self_employed_account import FormOrderPaymentSelfEmployedAccount
from handlers.advertiser.form_order.wallet import FormOrderWallet
from handlers.advertiser.personal_data.add_entity import AddDataEntityAdvertiser
from handlers.advertiser.personal_data.add_individual import AddDataIndividualAdvertiser
from handlers.advertiser.personal_data.add_self_employed_account import AddDataSelfEmployedAccountAdvertiser
from handlers.advertiser.personal_data.add_self_employed_card import AddDataSelfEmployedCardAdvertiser
from handlers.advertiser.personal_data.entity import PersonalDataEntityAdvertiser
from handlers.advertiser.personal_data.individual import PersonalDataIndividualAdvertiser
from handlers.advertiser.personal_data.personal_data import PersonalDataAdvertiser
from handlers.advertiser.personal_data.self_employed_account import PersonalDataSelfEmployedAccountAdvertiser
from handlers.advertiser.personal_data.self_employed_card import PersonalDataSelfEmployedCardAdvertiser
from handlers.advertiser.registration.entity import FirstEntityAdvertiser
from handlers.advertiser.registration.individual import FirstIndividualAdvertiser
from handlers.advertiser.registration.self_employed_account import FirstSelfEmployedAccountAdvertiser
from handlers.advertiser.registration.self_employed_card import FirstSelfEmployedCardAdvertiser
from handlers.advertiser.wallet.history import HistoryWalletAdvertiser
from handlers.advertiser.wallet.payment_common import PaymentCommonAdvertiser
from handlers.advertiser.wallet.payment_entity import PaymentEntityAdvertiser
from handlers.advertiser.wallet.payment_individual import PaymentIndividualAdvertiser
from handlers.advertiser.wallet.payment_self_employed import PaymentSelfEmployedAccountAdvertiser
from handlers.advertiser.wallet.wallet import WalletAdvertiser
from handlers.advertiser.wallet.withdraw_entity import WithdrawEntityAdvertiser
from handlers.advertiser.wallet.withdraw_individual import WithdrawIndividualAdvertiser
from handlers.advertiser.wallet.withdraw_self_employed_account import WithdrawSelfEmployedAccountAdvertiser
from handlers.advertiser.wallet.withdraw_self_employed_card import WithdrawSelfEmployedCardAdvertiser
from keyboards.reply.common.user import ReplyUser
from looping import pg, fastapi
from model.user import User
from text.advertiser.formMenu import FormMenuAdvertiser
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class MenuAdvertiser(StatesGroup):

    menuAdvertiser_level1 = State()
    menuAdvertiser_level2 = State()

    # main menu
    async def main_menu(self, message: types.Message, state: FSMContext):
        await self.menuAdvertiser_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await self._get_token(data=data)
            new_data = User(lang=data.get("lang"), email=data.get("email"), password=data.get("password"),
                            token=data.get("token"))
        await state.set_data(data=new_data)
        await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.menu,
                               reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _get_token(data):
        user = User(username=data.get("email"), password=data.get("password"))
        data['token'] = await fastapi.get_token(user=user)

    # menu change role
    async def menu_change_role(self, message: types.Message, state: FSMContext):
        await self.menuAdvertiser_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await fastapi.change_role(role="advertiser", token=data.get("token"))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.change,
                                   reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    # settings
    async def menu_setting(self, message: types.Message, state: FSMContext):
        await self.menuAdvertiser_level2.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.start.language,
                                   reply_markup=await reply.setting())

    async def menu_change_language(self, message: types.Message, state: FSMContext):
        await self.menuAdvertiser_level1.set()
        async with state.proxy() as data:
            data['lang'] = await self._change_language(message)
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.menu,
                                   reply_markup=await reply.menu_advertiser(login=data['email'], password=data['password']))

    @staticmethod
    async def _change_language(message):
        new_language = message.text
        user_id = message.from_user.id
        if new_language == Txt.settings.rus:
            language = Txt.rus_var
        elif new_language == Txt.settings.uzb:
            language = Txt.uzb_var
        else:
            return Txt.uzb_var
        await pg.update_language(language=language, user_id=user_id)
        return language

    async def menu_information(self, message: types.Message, state: FSMContext):
        await self.menuAdvertiser_level2.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.information,
                                   reply_markup=await reply.information())

    @staticmethod
    async def menu_about_us(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuAdvertiser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.about_us(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_how_to_use(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuAdvertiser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.how_to_use(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_feedback(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.feedback.feedback)



    # register_handler
    def register_handlers_menu_advertiser(self, dp: Dispatcher):

        dp.register_message_handler(self.main_menu, text=Txt.menu.menu,                                                 state=[*MenuAdvertiser.states_names,

                                                                                                                               *FirstEntityAdvertiser.states_names,
                                                                                                                               *FirstIndividualAdvertiser.states_names,
                                                                                                                               *FirstSelfEmployedAccountAdvertiser.states_names,
                                                                                                                               *FirstSelfEmployedCardAdvertiser.states_names,

                                                                                                                               "RegistrationAdvertiser:regAdvertiser_level5",
                                                                                                                                "RegistrationAdvertiser:regAdvertiser_level6",

                                                                                                                               *PersonalDataAdvertiser.states_names,
                                                                                                                               *PersonalDataEntityAdvertiser.states_names,
                                                                                                                               *PersonalDataIndividualAdvertiser.states_names,
                                                                                                                               *PersonalDataSelfEmployedAccountAdvertiser.states_names,
                                                                                                                               *PersonalDataSelfEmployedCardAdvertiser.states_names,

                                                                                                                               *AddDataEntityAdvertiser.states_names,
                                                                                                                               *AddDataIndividualAdvertiser.states_names,
                                                                                                                               *AddDataSelfEmployedAccountAdvertiser.states_names,
                                                                                                                               *AddDataSelfEmployedCardAdvertiser.states_names,

                                                                                                                               *WalletAdvertiser.states_names,
                                                                                                                               *PaymentEntityAdvertiser.states_names,
                                                                                                                               *PaymentIndividualAdvertiser.states_names,
                                                                                                                               *PaymentSelfEmployedAccountAdvertiser.states_names,
                                                                                                                               *PaymentCommonAdvertiser.states_names,

                                                                                                                               *WithdrawEntityAdvertiser.states_names,
                                                                                                                               *WithdrawIndividualAdvertiser.states_names,
                                                                                                                               *WithdrawSelfEmployedAccountAdvertiser.states_names,
                                                                                                                               *WithdrawSelfEmployedCardAdvertiser.states_names,
                                                                                                                               *HistoryWalletAdvertiser.states_names,
                                                                                                                               
                                                                                                                               *FormOrderAdvertiser.states_names,
                                                                                                                               *FormOrderPaymentCommon.states_names,
                                                                                                                               *FormOrderPaymentSelfEmployedAccount.states_names,
                                                                                                                               *FormOrderPaymentEntity.states_names,
                                                                                                                               *FormOrderPaymentIndividual.states_names,
                                                                                                                               *FormOrderWallet.states_names,
                                                                                                                               *AllOrderAdvertiser.states_names])

        dp.register_message_handler(self.menu_change_role, text=Txt.menu.change_blogger,                                state="MenuBlogger:menuBlogger_level1")

        dp.register_message_handler(self.main_menu, text=Txt.menu.nextTime,                                             state=["RegistrationAdvertiser:regAdvertiser_level5",
                                                                                                                               "RegistrationAdvertiser:regAdvertiser_level6",
                                                                                                                               *FirstEntityAdvertiser.states_names,
                                                                                                                               *FirstIndividualAdvertiser.states_names,
                                                                                                                               *FirstSelfEmployedAccountAdvertiser.states_names,
                                                                                                                               *FirstSelfEmployedCardAdvertiser.states_names,
                                                                                                                               ])

        dp.register_message_handler(self.menu_information, text=Txt.menu.information,                                   state=self.menuAdvertiser_level1)
        dp.register_message_handler(self.menu_about_us, text=Txt.information.about_us,                                  state=self.menuAdvertiser_level2)
        dp.register_message_handler(self.menu_how_to_use, text=Txt.information.how_to_use,                              state=self.menuAdvertiser_level2)
        dp.register_message_handler(self.menu_feedback, text=Txt.information.feedback,                                  state=self.menuAdvertiser_level2)

        dp.register_message_handler(self.menu_setting, text=Txt.menu.lang,                                              state=self.menuAdvertiser_level1)
        dp.register_message_handler(self.menu_change_language, text=Txt.settings.language,                              state=self.menuAdvertiser_level2)




