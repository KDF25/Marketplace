from math import ceil
from string import Template
import datetime
from datetime_now import dt_now
from text.language.main import Text_main
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()
nds = 1 + Txt.commission.nds / 100
bot_commission = 1 - Txt.commission.bot / 100


class FormSelfEmployedAccountData:

    def __init__(self, data: dict, language: str, email: str = None):
        self.__data = data
        self.__email = email
        self.__Lang = Txt.language[language]

    async def _unpack(self):
        self.__fio_user = self.__data.get("fio", "...")
        self.__number_user = self.__data.get("number", "...")
        self.__date_user = self.__data.get("date", "...")
        self.__pinfl_user = self.__data.get("pinfl", "...")
        self.__paymentAccount_user = self.__data.get("paymentAccount", "...")
        self.__bank_user = self.__data.get("bank", "...")
        self.__mfo_user = self.__data.get("mfo", "...")
        self.__phone_user = self.__data.get("phone", "...")

    async def menu_personal_data(self):
        await self._unpack()
        text = Template("<b>$account:</b> $account_user\n\n"
                        "$data\n\n"
                        "<b>$fio:</b> $fio_user\n"
                        "<b>$number:</b> $number_user\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user\n\n"
                        "$alright")
        text = text.substitute(account=self.__Lang.personalData.common.account, account_user=self.__email,
                               data=self.__Lang.personalData.common.data,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.pinfl, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user,
                               alright=self.__Lang.personalData.common.alright)
        return text

    async def menu_change_data(self):
        await self._unpack()
        text = Template("<b>$fio:</b> $fio_user\n"
                        "<b>$number:</b> $number_user\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user\n\n"
                        "$change_data")
        text = text.substitute(data=self.__Lang.personalData.common.data,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.pinfl, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user,
                               change_data=self.__Lang.personalData.common.changeData)
        return text

    async def menu_payment(self):
        await self._unpack()
        text = Template("$didox\n\n"
                        "<b>$title2:</b> Venkon Digital\n"
                        "<b>$inn:</b> 301490230\n"
                        "<b>$amount:</b> $cash $sum $nds\n\n"
                        "$data\n\n"
                        "<b>$fio:</b> $fio_user\n"
                        "<b>$number:</b> $number_user\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user\n\n")
        text = text.substitute(didox=self.__Lang.wallet.didox, title2=self.__Lang.personalData.common.title2,
                               amount=self.__Lang.wallet.payment, cash=await func.int_to_str(num=ceil(int(self.__data.get('cash')) * nds)),
                               sum=self.__Lang.wallet.sum, inn=self.__Lang.personalData.common.inn,
                               data=self.__Lang.personalData.common.data, nds=self.__Lang.wallet.payment_start.nds,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.pinfl, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user)
        return text

    async def menu_withdraw(self):
        await self._unpack()
        text = Template("<b>$credit:</b> $cash $sum\n"
                        "$operationDay — $day\n\n"
                        "$data\n\n"
                        "<b>$fio:</b> $fio_user\n"
                        "<b>$number:</b> $number_user\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$pinfl:</b> $pinfl_user\n"
                        "<b>$paymentAccount:</b> $paymentAccount_user\n"
                        "<b>$bank:</b> $bank_user\n"
                        "<b>$mfo:</b> $mfo_user\n"
                        "<b>$phone:</b> $phone_user\n\n"
                        "$alright")
        text = text.substitute(credit=self.__Lang.wallet.credit, cash=await func.int_to_str(num=ceil(self.__data.get('cash') * bot_commission)),
                               sum=self.__Lang.wallet.sum, operationDay=self.__Lang.wallet.operationDay, day="bla bla",
                               data=self.__Lang.personalData.common.data,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.pinfl, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user,
                               alright=self.__Lang.personalData.common.alright)
        return text

    async def menu_group(self):
        await self._unpack()
        date = datetime.datetime.strftime(dt_now.now(), "%d.%m.%Y")
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
                               today=date, method=self.__Lang.wallet.method, selfEmployed=self.__Lang.wallet.selfEmployedCard,
                               credit=self.__Lang.wallet.credit, cash=await func.int_to_str(num=ceil(self.__data.get('cash') * bot_commission)),
                               sum=self.__Lang.wallet.sum,
                               fio=self.__Lang.personalData.common.fio, fio_user=self.__fio_user,
                               number=self.__Lang.personalData.common.number, number_user=self.__number_user,
                               date=self.__Lang.personalData.common.date, date_user=self.__date_user,
                               pinfl=self.__Lang.personalData.common.pinfl, pinfl_user=self.__pinfl_user,
                               paymentAccount=self.__Lang.personalData.common.paymentAccount,
                               paymentAccount_user=self.__paymentAccount_user,
                               bank=self.__Lang.personalData.common.bank, bank_user=self.__bank_user,
                               mfo=self.__Lang.personalData.common.mfo, mfo_user=self.__mfo_user,
                               phone=self.__Lang.personalData.common.phone, phone_user=self.__phone_user)
        return text
