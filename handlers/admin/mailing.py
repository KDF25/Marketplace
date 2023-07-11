import asyncio
from contextlib import suppress

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked, Unauthorized, MessageNotModified, MessageToEditNotFound, \
    MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted, ChatNotFound

from config import bot
from filters.admin import IsAdmin
from keyboards.inline.admin.admin import InlineAdmin
from looping import pg
from text.admin.formAdmin import FormAdmin
from text.language.main import Text_main

Txt = Text_main()
inline = InlineAdmin()
form = FormAdmin()
main_text = "Администраторская"


class Mailing(StatesGroup):
    mailing_level1 = State()
    mailing_level2 = State()
    mailing_level3 = State()

    async def menu_check(self, message: types.Message, state: FSMContext):
        await self.next()
        async with state.proxy() as data:
            data["message_id"] = message.message_id
        await bot.copy_message(chat_id=message.from_user.id, message_id=message.message_id, from_chat_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text="Все верно?", reply_markup=await inline.menu_send())

    async def menu_send(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Рассылка началась')
            await self._mail_send(call, data)
        await bot.send_message(chat_id=call.from_user.id, text=main_text, reply_markup=await inline.menu_admin())
        await state.set_state("MenuAdmin:menu_admin_level1")

    @staticmethod
    async def _mail_send(call, data):
        users = await pg.get_all_users()
        index = 0
        for user in users:
            try:
                await bot.copy_message(chat_id=[*user][0], message_id=data.get("message_id"), from_chat_id=call.from_user.id)
                await asyncio.sleep(delay=0.05)
                index += 1
                if index % 100 == 0:
                    with suppress(MessageNotModified, MessageToEditNotFound):
                        await bot.edit_message_text(chat_id=call.from_user.id,  message_id=call.message.message_id,
                                                    text=f'Разослано {index} пользователям')
            except (BotBlocked, Unauthorized, ChatNotFound):
                await pg.block_status(user_id=[*user][0], status=False)
        else:
            with suppress(MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id,  text=await form.mail_end())

    @staticmethod
    async def menu_cancel(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text="Рассылка отменена")

    def register_handlers_mailing(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_check, IsAdmin(), content_types=["text", "photo", "video"], state=self.mailing_level1)
        dp.register_callback_query_handler(self.menu_send, IsAdmin(), text="yes", state=self.mailing_level2)
        dp.register_callback_query_handler(self.menu_cancel, IsAdmin(), text="cancel", state=self.mailing_level2)



