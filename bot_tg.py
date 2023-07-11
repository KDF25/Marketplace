from aiogram.utils import executor

from config import dp
from handlers.admin.statistics import Statistics

from handlers.common.menu import MenuCommon
from handlers.common.post_view import PostView
from handlers.common.new_message import NewMessage

from handlers.blogger.registration.registration import RegistrationBlogger
from handlers.blogger.registration.exist_account import ExistBlogger
from handlers.blogger.registration.platform import FirstPlatformBlogger
from handlers.blogger.registration.entity import FirstEntityBlogger
from handlers.blogger.registration.individual import FirstIndividualBlogger
from handlers.blogger.registration.self_employed_account import FirstSelfEmployedAccountBlogger
from handlers.blogger.registration.self_employed_card import FirstSelfEmployedCardBlogger
from handlers.blogger.menu import MenuBlogger

from handlers.blogger.personal_data.personal_data import PersonalDataBlogger
from handlers.blogger.personal_data.entity import PersonalDataEntityBlogger
from handlers.blogger.personal_data.individual import PersonalDataIndividualBlogger
from handlers.blogger.personal_data.self_employed_account import PersonalDataSelfEmployedAccountBlogger
from handlers.blogger.personal_data.self_employed_card import PersonalDataSelfEmployedCardBlogger
from handlers.blogger.personal_data.add_entity import AddDataEntityBlogger
from handlers.blogger.personal_data.add_individual import AddDataIndividualBlogger
from handlers.blogger.personal_data.add_self_employed_account import AddDataSelfEmployedAccountBlogger
from handlers.blogger.personal_data.add_self_employed_card import AddDataSelfEmployedCardBlogger

from handlers.blogger.wallet.wallet import WalletBlogger
from handlers.blogger.wallet.payment_common import PaymentCommonBlogger
from handlers.blogger.wallet.payment_entity import PaymentEntityBlogger
from handlers.blogger.wallet.payment_individual import PaymentIndividualBlogger
from handlers.blogger.wallet.payment_self_employed import PaymentSelfEmployedAccountBlogger

from handlers.blogger.wallet.withdraw_entity import WithdrawEntityBlogger
from handlers.blogger.wallet.withdraw_individual import WithdrawIndividualBlogger
from handlers.blogger.wallet.withdraw_self_employed_account import WithdrawSelfEmployedAccountBlogger
from handlers.blogger.wallet.withdraw_self_employed_card import WithdrawSelfEmployedCardBlogger
from handlers.blogger.wallet.history import HistoryWalletBlogger

from handlers.blogger.platform.all_platform import PlatformBlogger
from handlers.blogger.platform.add_platform import AddPlatformBlogger
from handlers.blogger.platform.change_platforn import ChangePlatformBlogger
from handlers.blogger.platform.delete_platform import DeletePlatformBlogger
from handlers.blogger.platform.calendar import CalendarBlogger
from handlers.blogger.all_orders.all_orders import AllOrderBlogger
from handlers.blogger.new_order import NewPostBlogger

from handlers.advertiser.registration.registration import RegistrationAdvertiser
from handlers.advertiser.registration.exist_account import ExistAdvertiser
from handlers.advertiser.registration.entity import FirstEntityAdvertiser
from handlers.advertiser.registration.individual import FirstIndividualAdvertiser
from handlers.advertiser.registration.self_employed_account import FirstSelfEmployedAccountAdvertiser
from handlers.advertiser.registration.self_employed_card import FirstSelfEmployedCardAdvertiser

from handlers.advertiser.menu import MenuAdvertiser

from handlers.advertiser.personal_data.personal_data import PersonalDataAdvertiser
from handlers.advertiser.personal_data.entity import PersonalDataEntityAdvertiser
from handlers.advertiser.personal_data.individual import PersonalDataIndividualAdvertiser
from handlers.advertiser.personal_data.self_employed_account import PersonalDataSelfEmployedAccountAdvertiser
from handlers.advertiser.personal_data.self_employed_card import PersonalDataSelfEmployedCardAdvertiser
from handlers.advertiser.personal_data.add_entity import AddDataEntityAdvertiser
from handlers.advertiser.personal_data.add_individual import AddDataIndividualAdvertiser
from handlers.advertiser.personal_data.add_self_employed_account import AddDataSelfEmployedAccountAdvertiser
from handlers.advertiser.personal_data.add_self_employed_card import AddDataSelfEmployedCardAdvertiser

from handlers.advertiser.wallet.wallet import WalletAdvertiser
from handlers.advertiser.wallet.payment_common import PaymentCommonAdvertiser
from handlers.advertiser.wallet.payment_entity import PaymentEntityAdvertiser
from handlers.advertiser.wallet.payment_individual import PaymentIndividualAdvertiser
from handlers.advertiser.wallet.payment_self_employed import PaymentSelfEmployedAccountAdvertiser

from handlers.advertiser.wallet.withdraw_entity import WithdrawEntityAdvertiser
from handlers.advertiser.wallet.withdraw_individual import WithdrawIndividualAdvertiser
from handlers.advertiser.wallet.withdraw_self_employed_account import WithdrawSelfEmployedAccountAdvertiser
from handlers.advertiser.wallet.withdraw_self_employed_card import WithdrawSelfEmployedCardAdvertiser
from handlers.advertiser.wallet.history import HistoryWalletAdvertiser

from handlers.advertiser.form_order.form_order import FormOrderAdvertiser
from handlers.advertiser.form_order.wallet import FormOrderWallet
from handlers.advertiser.form_order.payment_common import FormOrderPaymentCommon
from handlers.advertiser.form_order.payment_entity import FormOrderPaymentEntity
from handlers.advertiser.form_order.payment_individual import FormOrderPaymentIndividual
from handlers.advertiser.form_order.payment_self_employed_account import FormOrderPaymentSelfEmployedAccount
from handlers.advertiser.all_orders.all_orders import AllOrderAdvertiser
from handlers.advertiser.basket import BasketAdvertiser
from handlers.advertiser.post_moderation import PostModerationAdvertiser

from handlers.group.menu import MenuGroup
from handlers.group.withdraw import WithdrawGroup
from handlers.group.moderation import ModerationGroup
from handlers.group.post_view import FavorPostView
from handlers.group.post_moderation import PostModerationGroup
from handlers.group.ban_platfrom import BanPlatformGroup

from handlers.admin.menu import MenuAdmin
from handlers.admin.mailing import Mailing

from aiohttp import web
from looping import pg, fastapi


async def on_startup(dp):
	await pg.sql_start()
	await fastapi.fastapi_start()
	print("бот вышел в онлайн")

app = web.Application()

# class handler
# start common
menu_common = MenuCommon()

# main menu blogger
menu_blogger = MenuBlogger()

# post view
post_view = PostView()

# start blogger
reg_blogger = RegistrationBlogger()
exist_blogger = ExistBlogger()

# blogger first registration
first_platform = FirstPlatformBlogger()
first_entity_blogger = FirstEntityBlogger()
first_individual_blogger = FirstIndividualBlogger()
first_self_employed_account_blogger = FirstSelfEmployedAccountBlogger()
first_self_employed_card_blogger = FirstSelfEmployedCardBlogger()

# personal data blogger
data_blogger = PersonalDataBlogger()

entity_blogger = PersonalDataEntityBlogger()
individual_blogger = PersonalDataIndividualBlogger()
self_employed_account_blogger = PersonalDataSelfEmployedAccountBlogger()
self_employed_card_blogger = PersonalDataSelfEmployedCardBlogger()

add_entity_blogger = AddDataEntityBlogger()
add_individual_blogger = AddDataIndividualBlogger()
add_self_employed_account_blogger = AddDataSelfEmployedAccountBlogger()
add_self_employed_card_blogger = AddDataSelfEmployedCardBlogger()

# wallet blogger
wallet_blogger = WalletBlogger()
entity_payment_blogger = PaymentEntityBlogger()
individual_payment_blogger = PaymentIndividualBlogger()
self_employed_payment_blogger = PaymentSelfEmployedAccountBlogger()
common_payment_blogger = PaymentCommonBlogger()

withdraw_entity_blogger = WithdrawEntityBlogger()
withdraw_individual_blogger = WithdrawIndividualBlogger()
withdraw_self_employed_account_blogger = WithdrawSelfEmployedAccountBlogger()
withdraw_self_employed_card_blogger = WithdrawSelfEmployedCardBlogger()

history_wallet_blogger = HistoryWalletBlogger()

# platform blogger
platform_blogger = PlatformBlogger()
add_platform = AddPlatformBlogger()
change_platform = ChangePlatformBlogger()
delete_platform = DeletePlatformBlogger()
calendar_blogger = CalendarBlogger()

# new post
new_post_blogger = NewPostBlogger()

# all order advertiser
all_orders_blogger = AllOrderBlogger()

# main menu advertiser
menu_advertiser = MenuAdvertiser()

# start advertiser
reg_advertiser = RegistrationAdvertiser()
exist_advertiser = ExistAdvertiser()

# advertiser first registration
first_entity_advertiser = FirstEntityAdvertiser()
first_individual_advertiser = FirstIndividualAdvertiser()
first_self_employed_account_advertiser = FirstSelfEmployedAccountAdvertiser()
first_self_employed_card_advertiser = FirstSelfEmployedCardAdvertiser()

# personal data advertiser
data_advertiser = PersonalDataAdvertiser()

entity_advertiser = PersonalDataEntityAdvertiser()
individual_advertiser = PersonalDataIndividualAdvertiser()
self_employed_account_advertiser = PersonalDataSelfEmployedAccountAdvertiser()
self_employed_card_advertiser = PersonalDataSelfEmployedCardAdvertiser()

add_entity_advertiser = AddDataEntityAdvertiser()
add_individual_advertiser = AddDataIndividualAdvertiser()
add_self_employed_account_advertiser = AddDataSelfEmployedAccountAdvertiser()
add_self_employed_card_advertiser = AddDataSelfEmployedCardAdvertiser()

# wallet advertiser
wallet_advertiser = WalletAdvertiser()
entity_payment_advertiser = PaymentEntityAdvertiser()
individual_payment_advertiser = PaymentIndividualAdvertiser()
self_employed_payment_advertiser = PaymentSelfEmployedAccountAdvertiser()
common_payment_advertiser = PaymentCommonAdvertiser()

withdraw_entity_advertiser = WithdrawEntityAdvertiser()
withdraw_individual_advertiser = WithdrawIndividualAdvertiser()
withdraw_self_employed_account_advertiser = WithdrawSelfEmployedAccountAdvertiser()
withdraw_self_employed_card_advertiser = WithdrawSelfEmployedCardAdvertiser()
history_wallet_advertiser = HistoryWalletAdvertiser()

# form order advertiser
form_order_advertiser = FormOrderAdvertiser()
form_order_wallet = FormOrderWallet()
form_order_payment_common = FormOrderPaymentCommon()
form_order_payment_self_employed = FormOrderPaymentSelfEmployedAccount()
form_order_payment_entity = FormOrderPaymentEntity()
form_order_payment_individual = FormOrderPaymentIndividual()

# basket advertiser
basket_advertiser = BasketAdvertiser()

# all order advertiser
all_orders_advertiser = AllOrderAdvertiser()

# post moderation advertiser
post_moderation_advertiser = PostModerationAdvertiser()


# moderator
# menu group

menu_group = MenuGroup()
withdraw_group = WithdrawGroup()
moderation_group = ModerationGroup()
post_view_group = FavorPostView()
post_moderation_group = PostModerationGroup()
ban_platform_group = BanPlatformGroup()

# new message
new_message = NewMessage()

# admin
menu_admin = MenuAdmin()
menu_mailing = Mailing()
menu_statistics = Statistics()



# handlers registration
# common start
menu_common.register_handlers_menu_common(dp=dp)

# post view
post_view.register_handlers_post(dp=dp)

# blogger start
reg_blogger.register_handlers_registration_blogger(dp=dp)
exist_blogger.register_handlers_exist_blogger(dp=dp)

# main menu blogger
menu_blogger.register_handlers_menu_blogger(dp=dp)

# blogger first registration
first_platform.register_handlers_first_platform(dp=dp)

first_entity_blogger.register_handlers(dp=dp)
first_individual_blogger.register_handlers(dp=dp)
first_self_employed_account_blogger.register_handlers(dp=dp)
first_self_employed_card_blogger.register_handlers(dp=dp)

# personal data blogger
data_blogger.register_handlers_personal_data(dp=dp)

entity_blogger.register_handlers(dp=dp)
individual_blogger.register_handlers(dp=dp)
self_employed_account_blogger.register_handlers(dp=dp)
self_employed_card_blogger.register_handlers(dp=dp)

add_entity_blogger.register_handlers_personal(dp=dp)
add_individual_blogger.register_handlers_personal(dp=dp)
add_self_employed_account_blogger.register_handlers(dp=dp)
add_self_employed_card_blogger.register_handlers(dp=dp)

# wallet blogger
wallet_blogger.register_handlers(dp=dp)
entity_payment_blogger.register_handlers(dp=dp)
individual_payment_blogger.register_handlers(dp=dp)
self_employed_payment_blogger.register_handlers(dp=dp)
common_payment_blogger.register_handlers(dp=dp)

withdraw_entity_blogger.register_handlers(dp=dp)
withdraw_individual_blogger.register_handlers(dp=dp)
withdraw_self_employed_account_blogger.register_handlers(dp=dp)
withdraw_self_employed_card_blogger.register_handlers(dp=dp)
history_wallet_blogger.register_handlers(dp=dp)

# platform blogger
platform_blogger.register_handlers_platform_blogger(dp=dp)
add_platform.register_handlers_add_platform_blogger(dp=dp)
change_platform.register_handlers_change_platform_blogger(dp=dp)
delete_platform.register_handlers_delete_platform_blogger(dp=dp)
calendar_blogger.register_handlers_calendar(dp=dp)

# new post blogger
new_post_blogger.register_handlers_new_post(dp=dp)

# all order blogger
all_orders_blogger.register_handlers_all_orders_blogger(dp=dp)

# advertiser start
reg_advertiser.register_handlers_registration_advertiser(dp=dp)
exist_advertiser.register_handlers_exist_advertiser(dp=dp)

# main menu advertiser
menu_advertiser.register_handlers_menu_advertiser(dp=dp)

# advertiser first registration
first_entity_advertiser.register_handlers(dp=dp)
first_individual_advertiser.register_handlers(dp=dp)
first_self_employed_account_advertiser.register_handlers(dp=dp)
first_self_employed_card_advertiser.register_handlers(dp=dp)

# personal data advertiser
data_advertiser.register_handlers_personal_data(dp=dp)

entity_advertiser.register_handlers(dp=dp)
individual_advertiser.register_handlers(dp=dp)
self_employed_account_advertiser.register_handlers(dp=dp)
self_employed_card_advertiser.register_handlers(dp=dp)

add_entity_advertiser.register_handlers_personal(dp=dp)
add_individual_advertiser.register_handlers_personal(dp=dp)
add_self_employed_account_advertiser.register_handlers(dp=dp)
add_self_employed_card_advertiser.register_handlers(dp=dp)

# wallet advertiser
wallet_advertiser.register_handlers(dp=dp)
entity_payment_advertiser.register_handlers(dp=dp)
individual_payment_advertiser.register_handlers(dp=dp)
self_employed_payment_advertiser.register_handlers(dp=dp)
common_payment_advertiser.register_handlers(dp=dp)

withdraw_entity_advertiser.register_handlers(dp=dp)
withdraw_individual_advertiser.register_handlers(dp=dp)
withdraw_self_employed_account_advertiser.register_handlers(dp=dp)
withdraw_self_employed_card_advertiser.register_handlers(dp=dp)
history_wallet_advertiser.register_handlers(dp=dp)

# form order advertiser
form_order_advertiser.register_handlers_form_order(dp=dp)
form_order_wallet.register_handlers_form_order_wallet(dp=dp)
form_order_payment_common.register_handlers_form_order_payment(dp=dp)
form_order_payment_entity.register_handlers(dp=dp)
form_order_payment_individual.register_handlers(dp=dp)
form_order_payment_self_employed.register_handlers(dp=dp)

# basket advertiser
basket_advertiser.register_handlers_basket(dp=dp)

# all order advertiser
all_orders_advertiser.register_handlers_all_orders_advertiser(dp=dp)

# post moderation advertiser
post_moderation_advertiser.register_handlers(dp=dp)

# moderator
# menu group
menu_group.register_handlers_menu_group(dp=dp)
withdraw_group.register_handlers_withdraw(dp=dp)
moderation_group.register_handlers_moderation(dp=dp)
post_view_group.register_handlers_post(dp=dp)
post_moderation_group.register_handlers_moderation(dp=dp)
ban_platform_group.register_handlers_ban_platform(dp=dp)

# admin
menu_admin.register_handlers_menu_admin(dp=dp)
menu_mailing.register_handlers_mailing(dp=dp)
menu_statistics.register_handlers_statistics(dp=dp)


# new message
new_message.register_handlers(dp=dp)


executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)

