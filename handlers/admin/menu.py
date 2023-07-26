from contextlib import suppress

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from config import bot
from filters.admin import IsAdmin
from handlers.admin.mailing import Mailing
from handlers.admin.statistics import Statistics
from keyboards.inline.admin.admin import InlineAdmin
from keyboards.reply.common.user import ReplyUser
from text.language.main import Text_main
from text.language.ru import Ru_language as Model

Txt = Text_main()
reply = ReplyUser(language='rus')
inline = InlineAdmin()

main_text = "Администраторская"


class MenuAdmin(StatesGroup):
    menu_admin_level1 = State()

    async def start_admin(self, message: types.Message, state: FSMContext):
        await bot.send_message(chat_id=message.from_user.id, text=main_text,  reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=message.from_user.id, text=main_text, reply_markup=await inline.menu_admin())
        await self.menu_admin_level1.set()

    async def main_menu(self, message: types.Message, state: FSMContext):
        await bot.send_message(chat_id=message.from_user.id, text=main_text, reply_markup=await inline.menu_admin())
        await self.menu_admin_level1.set()

    async def menu_back(self, call: types.CallbackQuery, state: FSMContext):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await self.menu_admin_level1.set()
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id,  text=main_text,
                                        reply_markup=await inline.menu_admin(), message_id=call.message.message_id)

    @staticmethod
    async def menu_mailing(call: types.CallbackQuery, state: FSMContext):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await Mailing.mailing_level1.set()
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text="Отправьте то, что хотели бы разослать!",
                                        reply_markup=await inline.menu_back(), message_id=call.message.message_id)

    @staticmethod
    async def menu_statistics(call: types.CallbackQuery, state: FSMContext):
        with suppress(MessageNotModified, MessageToEditNotFound):
            await Statistics.statistics_level1.set()
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, text="Выберите период",reply_markup=await inline.menu_period(),
                                        message_id=call.message.message_id)

    def register_handlers_menu_admin(self, dp: Dispatcher):
        dp.register_message_handler(self.start_admin, IsAdmin(), commands="admin", state='*')
        dp.register_message_handler(self.main_menu, IsAdmin(), text=Txt.menu.menu, state=[*Mailing.states_names, self.menu_admin_level1])
        dp.register_callback_query_handler(self.menu_back, IsAdmin(), text="back", state=[Mailing.mailing_level1, Statistics.statistics_level1])
        dp.register_callback_query_handler(self.menu_mailing, IsAdmin(), text="mail", state=self.menu_admin_level1)

        dp.register_callback_query_handler(self.menu_statistics, IsAdmin(), text="statistics", state=self.menu_admin_level1)


