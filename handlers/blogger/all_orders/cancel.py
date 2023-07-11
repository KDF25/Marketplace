# from contextlib import suppress
# from typing import Union
#
# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import IsReplyFilter
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted, \
#     MessageToEditNotFound, BotBlocked
#
# from config import bot
# from filters.admin import IsAdmin
# from handlers.blogger.all_orders.send_advertiser import SendMessageAdvertiser
# from keyboards.inline.blogger.newPost import InlinePostBlogger
# from keyboards.inline.common.wallet import InlineWalletUser
# from keyboards.inline.group.user import InlineGroupUser
# from keyboards.reply.common.user import ReplyUser
# from looping import fastapi, pg
# from model.moderation import ModerationModel
# from text.blogger.formNewOrder import FormNewOrder
# from text.common.formWallet import FormWallet
# from text.group.formModeration import FormModerationGroup
# from text.language.main import Text_main
# from filters.personal_data import IsNumber
# from text.fuction.function import TextFunc
# from text.group.formWithdraw import FormWithdrawGroup
#
# Txt = Text_main()
# func = TextFunc()
#
#
# class CancelPostBlogger(StatesGroup):
#
#     accept_level1 = State()
#     reject_level1 = State()
#     cancel_level1 = State()
#     sendAdvertiser_level1 = State()
#
#     # menu project cancel
#     async def menu_project_cancel(self, call: types.CallbackQuery, state: FSMContext):
#         print(call.message)
#         async with state.proxy() as data:
#             Lang, inline = await self._prepare_cancel(call, data)
#             await self._cancel(call, Lang, inline)
#
#     @staticmethod
#     async def _prepare_cancel(call, data):
#         blogger_area_id = int(call.data.split("_")[1])
#         Lang = Txt.language[data.get('lang')]
#         inline = InlinePostBlogger(language=data.get('lang'),  blogger_area_id=blogger_area_id)
#         return Lang, inline
#
#     @staticmethod
#     async def _cancel(call, Lang, inline):
#         with suppress(MessageNotModified, MessageToEditNotFound):
#             await call.answer()
#             await bot.edit_message_text(chat_id=call.from_user.id,  message_id=call.message.message_id,
#                                         text=Lang.newOrder.blogger.cancel,  reply_markup=await inline.menu_back())
#
#     # menu project reject
#     async def menu_project_reject(self, call: types.CallbackQuery, state: FSMContext):
#         async with state.proxy() as data:
#             status, json = await self._post_reject(call, data=data)
#             await self._check_reject(call, data, status, json)
#
#     @staticmethod
#     async def _post_reject(call, data):
#         blogger_area_id = int(call.data.split("_")[1])
#         json = {"blogger_area_id": blogger_area_id}
#         status, json = await fastapi.blogger_reject(json=json, token=data.get("token"))
#         return status, json
#
#     async def _check_reject(self, call, data, status, json):
#         Lang, inline = await self._prepare_cancel(call, data)
#         if status == 200:
#             await self._reject(call, Lang, json)
#         else:
#             await call.answer(text=Lang.alert.common.error, show_alert=True)
#
#     async def _reject(self, call, Lang, json):
#         await self._blogger_reject(call, Lang)
#         await self._user_reject(json)
#
#     @staticmethod
#     async def _blogger_reject(call, Lang):
#         with suppress(MessageNotModified, MessageToEditNotFound):
#             await call.answer()
#             await bot.edit_message_text(chat_id=call.from_user.id, text=Lang.newOrder.blogger.cancel,
#                                         message_id=call.message.message_id)
#
#     @staticmethod
#     async def _user_reject(json):
#         users = await pg.select_users(client_id=json.get("advertiser_id"))
#         for user_id in users:
#             try:
#                 lang_user = await pg.select_language(user_id=user_id[0])
#                 form_user = FormNewOrder(language=lang_user, data=json)
#                 await bot.send_message(chat_id=user_id[0], text=await form_user.menu_reject(), disable_web_page_preview=True)
#             except BotBlocked:
#                 await pg.block_status(user_id=user_id[0], status=False)
#
#     # menu project cancel back
#     async def menu_project_cancel_back(self, call: types.CallbackQuery, state: FSMContext):
#         async with state.proxy() as data:
#             status, json = await self._project_blogger(call, data)
#             form, inline = await self._prepare_back(call, data, json)
#             await self._cancel_back(call, form, inline)
#
#     @staticmethod
#     async def _project_blogger(call, data):
#         blogger_area_id = int(call.data.split("_")[1])
#         status, json = await fastapi.project_blogger(blogger_area_id=blogger_area_id, token=data.get("token"))
#         return status, json
#
#     @staticmethod
#     async def _prepare_back(call, data, json):
#         order_id = int(call.data.split("_")[1])
#         form = FormNewOrder(language=data.get('lang'), data=json)
#         inline = InlinePostBlogger(language=data.get('lang'), client_id=json.get("advertiser_id"), order_id=order_id)
#         return form, inline
#
#     @staticmethod
#     async def _cancel_back(call, form, inline):
#         with suppress(MessageNotModified, MessageToEditNotFound):
#             await call.answer()
#             await bot.edit_message_text(chat_id=call.from_user.id, text=await form.menu_send_blogger(),
#                                         message_id=call.message.message_id, reply_markup=await inline.menu_new_post(),
#                                         disable_web_page_preview=True)
#
#     def register_handlers_new_post(self, dp: Dispatcher):
#         dp.register_callback_query_handler(self.menu_project_cancel, lambda x: x.data.startswith("PostCancel"),          state="*")
#         dp.register_callback_query_handler(self.menu_project_cancel_back, lambda x: x.data.startswith("CancelBack"),    state="*")
#         dp.register_callback_query_handler(self.menu_project_reject, lambda x: x.data.startswith("Reject"),             state="*")
#
#
#
#
#
#
