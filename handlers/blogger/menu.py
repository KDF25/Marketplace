from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from handlers.blogger.all_orders.all_orders import AllOrderBlogger
from handlers.blogger.personal_data.add_entity import AddDataEntityBlogger
from handlers.blogger.personal_data.add_individual import AddDataIndividualBlogger
from handlers.blogger.personal_data.add_self_employed_account import AddDataSelfEmployedAccountBlogger
from handlers.blogger.personal_data.add_self_employed_card import AddDataSelfEmployedCardBlogger
from handlers.blogger.personal_data.entity import PersonalDataEntityBlogger
from handlers.blogger.personal_data.individual import PersonalDataIndividualBlogger
from handlers.blogger.personal_data.personal_data import PersonalDataBlogger
from handlers.blogger.personal_data.self_employed_account import PersonalDataSelfEmployedAccountBlogger
from handlers.blogger.personal_data.self_employed_card import PersonalDataSelfEmployedCardBlogger
from handlers.blogger.platform.add_platform import AddPlatformBlogger
from handlers.blogger.platform.all_platform import PlatformBlogger
from handlers.blogger.platform.calendar import CalendarBlogger
from handlers.blogger.platform.change_platforn import ChangePlatformBlogger
from handlers.blogger.platform.delete_platform import DeletePlatformBlogger
from handlers.blogger.registration.entity import FirstEntityBlogger
from handlers.blogger.registration.individual import FirstIndividualBlogger
from handlers.blogger.registration.platform import FirstPlatformBlogger
from handlers.blogger.registration.self_employed_account import FirstSelfEmployedAccountBlogger
from handlers.blogger.registration.self_employed_card import FirstSelfEmployedCardBlogger
from handlers.blogger.wallet.history import HistoryWalletBlogger
from handlers.blogger.wallet.payment_common import PaymentCommonBlogger
from handlers.blogger.wallet.payment_entity import PaymentEntityBlogger
from handlers.blogger.wallet.payment_individual import PaymentIndividualBlogger
from handlers.blogger.wallet.payment_self_employed import PaymentSelfEmployedAccountBlogger
from handlers.blogger.wallet.wallet import WalletBlogger
from handlers.blogger.wallet.withdraw_entity import WithdrawEntityBlogger
from handlers.blogger.wallet.withdraw_individual import WithdrawIndividualBlogger
from handlers.blogger.wallet.withdraw_self_employed_account import WithdrawSelfEmployedAccountBlogger
from handlers.blogger.wallet.withdraw_self_employed_card import WithdrawSelfEmployedCardBlogger
from keyboards.reply.common.user import ReplyUser
from looping import pg, fastapi
from model.user import User
from text.blogger.formMenu import FormMenuBlogger
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()


class MenuBlogger(StatesGroup):

    menuBlogger_level1 = State()
    menuBlogger_level2 = State()

    # main menu
    async def main_menu(self, message: types.Message, state: FSMContext):
        print(await state.get_state())
        await self.menuBlogger_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await self._get_token(data=data)
            new_data = User(lang=data.get("lang"), email=data.get("email"), password=data.get("password"), token=data.get("token"))
        await state.set_data(data=new_data)
        await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.menu,
                               reply_markup=await reply.menu_blogger())

    @staticmethod
    async def _get_token(data):
        user = User(username=data.get("email"), password=data.get("password"))
        data['token'] = await fastapi.get_token(user=user)

    # menu change role
    async def menu_change_role(self, message: types.Message, state: FSMContext):
        await self.menuBlogger_level1.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.advertiser.change,
                                   reply_markup=await reply.menu_blogger())
            await fastapi.change_role(role="blogger", token=data.get("token"))

    # settings
    async def menu_setting(self, message: types.Message, state: FSMContext):
        await self.menuBlogger_level2.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.start.language,
                                   reply_markup=await reply.setting())

    async def menu_change_language(self, message: types.Message, state: FSMContext):
        await self.menuBlogger_level1.set()
        async with state.proxy() as data:
            data['lang'] = await self._change_language(message)
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.menu,
                                   reply_markup=await reply.menu_blogger())

    async def menu_information(self, message: types.Message, state: FSMContext):
        await self.menuBlogger_level2.set()
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            reply = ReplyUser(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Lang.menu.blogger.information,
                                   reply_markup=await reply.information())

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

    @staticmethod
    async def menu_about_us(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuBlogger(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.about_us(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_how_to_use(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuBlogger(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.how_to_use(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_feedback(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Lang: Model = Txt.language[data.get('lang')]
            await bot.send_message(chat_id=message.from_user.id, text=Lang.feedback.feedback)


    def register_handlers_menu_blogger(self, dp: Dispatcher):
        dp.register_message_handler(self.main_menu, text=Txt.menu.menu,                                                 state=[*MenuBlogger.states_names,

                                                                                                                               *FirstEntityBlogger.states_names,
                                                                                                                               *FirstIndividualBlogger.states_names,
                                                                                                                               *FirstSelfEmployedAccountBlogger.states_names,
                                                                                                                               *FirstSelfEmployedCardBlogger.states_names,

                                                                                                                               *FirstPlatformBlogger.states_names,
                                                                                                                               "RegistrationBlogger:regBlogger_level5",

                                                                                                                               *PersonalDataBlogger.states_names,
                                                                                                                               *PersonalDataEntityBlogger.states_names,
                                                                                                                               *PersonalDataIndividualBlogger.states_names,
                                                                                                                               *PersonalDataSelfEmployedAccountBlogger.states_names,
                                                                                                                               *PersonalDataSelfEmployedCardBlogger.states_names,

                                                                                                                               *AddDataEntityBlogger.states_names,
                                                                                                                               *AddDataIndividualBlogger.states_names,
                                                                                                                               *AddDataSelfEmployedAccountBlogger.states_names,
                                                                                                                               *AddDataSelfEmployedCardBlogger.states_names,

                                                                                                                               *WalletBlogger.states_names,
                                                                                                                               *PaymentEntityBlogger.states_names,
                                                                                                                               *PaymentIndividualBlogger.states_names,
                                                                                                                               *PaymentSelfEmployedAccountBlogger.states_names,
                                                                                                                               *PaymentCommonBlogger.states_names,

                                                                                                                               *WithdrawEntityBlogger.states_names,
                                                                                                                               *WithdrawIndividualBlogger.states_names,
                                                                                                                               *WithdrawSelfEmployedAccountBlogger.states_names,
                                                                                                                               *WithdrawSelfEmployedCardBlogger.states_names,
                                                                                                                               *HistoryWalletBlogger.states_names,

                                                                                                                               *PlatformBlogger.states_names,
                                                                                                                               *AddPlatformBlogger.states_names,
                                                                                                                               *ChangePlatformBlogger.states_names,
                                                                                                                               *DeletePlatformBlogger.states_names,

                                                                                                                               *CalendarBlogger.states_names,
                                                                                                                               *AllOrderBlogger.states_names,
                                                                                                                               "NewPostBlogger:post_level1"])

        dp.register_message_handler(self.menu_change_role, text=Txt.menu.change_advertiser,                             state="MenuAdvertiser:menuAdvertiser_level1")
        dp.register_message_handler(self.main_menu, text=Txt.menu.nextTime,                                             state=["FirstPlatformBlogger:firstPlatform_level14",
                                                                                                                               "FirstPlatformBlogger:firstPlatform_level15",
                                                                                                                                *FirstEntityBlogger.states_names,
                                                                                                                                *FirstIndividualBlogger.states_names,
                                                                                                                                *FirstSelfEmployedAccountBlogger.states_names,
                                                                                                                                *FirstSelfEmployedCardBlogger.states_names])

        dp.register_message_handler(self.menu_information, text=Txt.menu.information,                                   state=self.menuBlogger_level1)
        dp.register_message_handler(self.menu_about_us, text=Txt.information.about_us,                                  state=self.menuBlogger_level2)
        dp.register_message_handler(self.menu_how_to_use, text=Txt.information.how_to_use,                              state=self.menuBlogger_level2)
        dp.register_message_handler(self.menu_feedback, text=Txt.information.feedback,                                  state=self.menuBlogger_level2)

        dp.register_message_handler(self.menu_setting, text=Txt.menu.lang,                                              state=self.menuBlogger_level1)
        dp.register_message_handler(self.menu_change_language, text=Txt.settings.language,                              state=self.menuBlogger_level2)



