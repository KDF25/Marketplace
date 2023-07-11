import datetime
from math import ceil
from string import Template

from datetime_now import dt_now
from text.language.main import Text_main
from text.fuction.function import TextFunc
Txt = Text_main()
func = TextFunc()
nds = 1 + Txt.commission.nds / 100
bot_commission = 1 - Txt.commission.bot / 100


class FormWithdrawGroup:

    def __init__(self, language: str, amount: int = None, text: str = None, data: dict = None):
        self.__text = text
        self.__amount = amount
        self.__data = data
        self.__Lang = Txt.language[language]

    async def menu_accept_user(self):
        text = Template("$accept\n\n"
                        "$cash — <b>$amount $sum</b>\n\n"
                        "$wallet")
        text = text.substitute(accept=self.__Lang.group.withdraw.user.accept, cash=self.__Lang.group.withdraw.user.cash,
                               amount=await func.int_to_str(num=ceil(int(self.__amount) * bot_commission)),
                               sum=self.__Lang.group.withdraw.user.sum, wallet=self.__Lang.group.withdraw.user.wallet)
        return text

    async def menu_reject_user(self):
        text = Template("$reject\n\n"
                        "<b>$reason:</b> $text\n\n"
                        "$back")
        text = text.substitute(reject=self.__Lang.group.withdraw.user.reject,
                               reason=self.__Lang.group.withdraw.user.reason, text=self.__text,
                               back=self.__Lang.group.withdraw.user.back)
        return text

    async def menu_on_withdraw(self):
        text = ""
        if self.__data.get("withdrawal_data").get("type_legal") == "entity":
            text = await self._entity()
        elif self.__data.get("withdrawal_data").get("type_legal") == "individual":
            text = await self._individual()
        elif self.__data.get("withdrawal_data").get("type_legal") == "self_employed":
            text = await self._self_employed_account()
        elif self.__data.get("withdrawal_data").get("type_legal") == "self_employed_transit":
            text = await self._self_employed_card()
        return text

    async def _entity(self):
        await self._unpack_entity()
        text = Template("<b>$request</b>\n"
                        "<b>$date_request:</b> $today\n\n"
                        "<b>$method:</b> $entity\n"
                        "<b>$credit:</b> $cash $sum\n\n"
                        "<b>$title:</b> $title_user\n"
                        "<b>$legalAddress:</b> $legalAddress_user\n"
                        "<b>$inn:</b> $inn_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user")
        text = text.substitute(request=self.__Lang.wallet.request, date_request=self.__Lang.wallet.date_request,
                               today=self.__date, method=self.__Lang.wallet.method, entity=self.__Lang.wallet.entity,
                               credit=self.__Lang.wallet.credit, cash=self.__cash,
                               sum=self.__Lang.wallet.sum,
                               title=self.__Lang.personalData.common.titleEntity, title_user=self.__title_user,
                               legalAddress=self.__Lang.personalData.common.legalAddress,
                               legalAddress_user=self.__legalAddress_user,
                               inn=self.__Lang.personalData.common.inn, inn_user=self.__inn_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user)
        return text

    async def _unpack_entity(self):
        self.__date = self.__data.get("withdrawal_data").get("date")
        self.__cash = await func.int_to_str(num=ceil(self.__data.get("withdrawal_data").get("amount") * bot_commission))
        self.__title_user = self.__data.get("entity").get("name")
        self.__legalAddress_user = self.__data.get("entity").get("legal_address")
        self.__inn_user = self.__data.get("entity").get("INN")
        self.__paymentAccount_user = self.__data.get("entity").get("payment_account")
        self.__bank_user = self.__data.get("entity").get("bank")
        self.__mfo_user = self.__data.get("entity").get("MFO")
        self.__phone_user = self.__data.get("entity").get("phone")

    async def _individual(self):
        await self._unpack_individual()
        text = Template("<b>$request</b>\n"
                        "<b>$date_request:</b> $today\n\n"
                        "<b>$method:</b> $individual\n"
                        "<b>$credit:</b> $cash $sum\n\n"
                        "<b>$title:</b> $title_user\n"
                        "<b>$legalAddress:</b> $legalAddress_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user")
        text = text.substitute(request=self.__Lang.wallet.request, date_request=self.__Lang.wallet.date_request,
                               today=self.__date, method=self.__Lang.wallet.method, individual=self.__Lang.wallet.individual,
                               credit=self.__Lang.wallet.credit, cash=self.__cash,
                               sum=self.__Lang.wallet.sum,
                               title=self.__Lang.personalData.common.titleIndividual, title_user=self.__title_user,
                               legalAddress=self.__Lang.personalData.common.legalAddress,
                               legalAddress_user=self.__legalAddress_user,
                               pinfl=self.__Lang.personalData.common.pinfl, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user)
        return text

    async def _unpack_individual(self):
        self.__date = self.__data.get("withdrawal_data").get("date")
        self.__cash = await func.int_to_str(num=ceil(self.__data.get("withdrawal_data").get("amount") * bot_commission))
        self.__title_user = self.__data.get("entity").get("name")
        self.__legalAddress_user = self.__data.get("entity").get("legal_address")
        self.__pinfl_user = self.__data.get("entity").get("PNFL")
        self.__paymentAccount_user = self.__data.get("entity").get("payment_account")
        self.__bank_user = self.__data.get("entity").get("bank")
        self.__mfo_user = self.__data.get("entity").get("MFO")
        self.__phone_user = self.__data.get("entity").get("phone")

    async def _self_employed_account(self):
        await self._unpack_self_employed_account()
        text = Template("<b>$request</b>\n"
                        "<b>$date_request:</b> $today\n\n"
                        "<b>$method:</b> $selfEmployed\n"
                        "<b>$credit:</b> $cash $sum\n\n"
                        "<b>$fio:</b> $fio_user\n"
                        "<b>$number:</b> $number_user\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user\n\n")
        text = text.substitute(request=self.__Lang.wallet.request, date_request=self.__Lang.wallet.date_request,
                               today=self.__date, method=self.__Lang.wallet.method,
                               selfEmployed=self.__Lang.wallet.selfEmployedCard, credit=self.__Lang.wallet.credit,
                               cash=self.__cash, sum=self.__Lang.wallet.sum,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.inn, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user)
        return text

    async def _unpack_self_employed_account(self):
        self.__date = self.__data.get("withdrawal_data").get("date")
        self.__cash = await func.int_to_str(num=ceil(self.__data.get("withdrawal_data").get("amount") * bot_commission))
        self.__fio_user = self.__data.get("entity").get("name")
        self.__number_user = self.__data.get("entity").get("number_registration")
        self.__date_user = self.__data.get("entity").get("date_registration")
        self.__pinfl_user = self.__data.get("entity").get("PNFL")
        self.__paymentAccount_user = self.__data.get("entity").get("payment_account")
        self.__bank_user = self.__data.get("entity").get("bank")
        self.__mfo_user = self.__data.get("entity").get("MFO")
        self.__phone_user = self.__data.get("entity").get("phone")

    async def _self_employed_card(self):
        await self._unpack_self_employed_card()
        text = Template("<b>$request</b>\n"
                        "<b>$date_request:</b> $today\n\n"
                        "<b>$method:</b> $selfEmployed\n"
                        "<b>$credit:</b> $cash $sum\n\n"
                        "<b>$fio:</b> $fio_user\n"
                        "<b>$number:</b> $number_user\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user\n"
                        "<b>$card_number:</b> $card_number_user\n"
                        "<b>$card_date:</b> $card_date_user\n\n")
        text = text.substitute(request=self.__Lang.wallet.request, date_request=self.__Lang.wallet.date_request,
                               today=self.__date, method=self.__Lang.wallet.method,
                               selfEmployed=self.__Lang.wallet.selfEmployedCard, credit=self.__Lang.wallet.credit,
                               cash=self.__cash, sum=self.__Lang.wallet.sum,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.inn, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.transitAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user,
                               card_number=self.__Lang.personalData.common.cardNumber, card_number_user=self.__card_number,
                               card_date=self.__Lang.personalData.common.cardDate, card_date_user=self.__card_date)
        return text

    async def _unpack_self_employed_card(self):
        self.__date = self.__data.get("withdrawal_data").get("date")
        self.__cash = await func.int_to_str(num=ceil(self.__data.get("withdrawal_data").get("amount") * bot_commission))
        self.__fio_user = self.__data.get("entity").get("name")
        self.__number_user = self.__data.get("entity").get("number_registration")
        self.__date_user = self.__data.get("entity").get("date_registration")
        self.__pinfl_user = self.__data.get("entity").get("PNFL")
        self.__paymentAccount_user = self.__data.get("entity").get("transit_account")
        self.__bank_user = self.__data.get("entity").get("bank")
        self.__mfo_user = self.__data.get("entity").get("MFO")
        self.__phone_user = self.__data.get("entity").get("phone")
        self.__card_number = self.__data.get("entity").get("card_number")
        self.__card_date = self.__data.get("entity").get("card_date")