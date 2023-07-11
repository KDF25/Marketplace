from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, moderation_chat_id
from filters.admin import IsAdmin
from handlers.group.ban_platfrom import BanPlatformGroup
from handlers.group.moderation import ModerationGroup
from handlers.group.on_ban_platform import OnBanPlatform
from handlers.group.on_moderation import OnModerationGroup
from handlers.group.on_withdraw import OnWithdrawGroup
from handlers.group.withdraw import WithdrawGroup
from keyboards.inline.common.common import Start
from keyboards.reply.group.user import ReplyUser
from looping import pg
from text.language.main import Text_main

Txt = Text_main()


class MenuGroup(StatesGroup):
    start = State()

    # menu moderator
    @staticmethod
    async def command_start(message: types.Message, state: FSMContext):
        reply = ReplyUser()
        await bot.send_message(chat_id=moderation_chat_id, text=".", reply_markup=await reply.menu_group())

    # menu reply
    async def menu_reply(self, message: types.Message, state: FSMContext):
        try:
            print(2222)
            await self.start.set()
            type_id = await self._unpack_reply(message=message)
            await self._type(type_id=type_id, message=message)
        except Exception:
            pass

    @staticmethod
    async def _unpack_reply(message: types.Message):
        entities = message.reply_to_message.entities
        type_id = entities[-1].get_text(message.reply_to_message.text).split('_')[0]
        return type_id

    @staticmethod
    async def _type(type_id: str, message: types.Message):
        Lang = Txt.language["rus"]
        if type_id == "#journalId":
            Class = WithdrawGroup()
            await Class.menu_withdraw_reject(message=message)
        elif type_id == "#areaId":
            Class = ModerationGroup()
            await Class.menu_moderation_reject(message=message)
        elif type_id == "#banId":
            Class = BanPlatformGroup()
            await Class.menu_ban(message=message)
        elif message.reply_to_message.html_text == Lang.banPlatform.group.start:
            ban_platform = OnBanPlatform()
            await ban_platform.start(message=message)

    # menu on moderation
    @staticmethod
    async def menu_moderation(message: types.Message, state: FSMContext):
        moderation = OnModerationGroup()
        await moderation.start()

    # menu on withdraw
    @staticmethod
    async def menu_withdraw(message: types.Message, state: FSMContext):
        withdraw = OnWithdrawGroup()
        await withdraw.start()

    @staticmethod
    async def menu_platform_find(message: types.Message, state: FSMContext):
        Lang = Txt.language["rus"]
        await bot.send_message(chat_id=moderation_chat_id, text=Lang.banPlatform.group.start)

    # register_handler
    def register_handlers_menu_group(self, dp: Dispatcher):
        dp.register_message_handler(self.command_start, IsAdmin(), commands="moderator",                                state="*")

        dp.register_message_handler(self.menu_moderation, IsAdmin(), text=Txt.group.moderation,                         state="*")
        dp.register_message_handler(self.menu_withdraw, IsAdmin(), text=Txt.group.withdraw,                             state="*")
        dp.register_message_handler(self.menu_platform_find, IsAdmin(), text=Txt.group.banPlatform,                     state="*")

        dp.register_message_handler(self.menu_reply, IsAdmin(), IsReplyFilter(is_reply=True), content_types="text",     state=self.start)
