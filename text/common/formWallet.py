from math import ceil
from string import Template

from aiogram.utils.markdown import hlink

from text.language.main import Text_main
from text.fuction.function import TextFunc

Txt = Text_main()
func = TextFunc()
nds = 1 + Txt.commission.nds / 100
bot_commission = 1 - Txt.commission.bot / 100

class FormWallet:

    def __init__(self, language: str, cash: int = None, data: dict = None, payment: int = None):
        self.__data = data
        self.__cash = cash
        self.__payment = payment
        self.__Lang = Txt.language[language]

    async def menu_payment_start(self):
        text = Template("<b>$cash:</b> $cash_payment $sum $nds\n\n"
                        "$choose")
        text = text.substitute(cash=self.__Lang.wallet.payment_start.cash,
                               cash_payment=await func.int_to_str(num=int(self.__data.get('cash') * nds)),
                               nds=self.__Lang.wallet.payment_start.nds,
                               choose=self.__Lang.wallet.payment_start.method,
                               sum=self.__Lang.wallet.sum)
        return text

    async def menu_payment_start2(self):
        text = Template("<b>$cash:</b> $cash_payment $sum $nds\n\n"
                        "$choose")
        text = text.substitute(cash=self.__Lang.wallet.payment_start.cash,
                               cash_payment=await func.int_to_str(num=int(self.__cash * nds)),
                               nds=self.__Lang.wallet.payment_start.nds,
                               choose=self.__Lang.wallet.payment_start.method,
                               sum=self.__Lang.wallet.sum)
        return text

    async def menu_wallet(self):
        text = Template("<b>$balance:</b> $wallet $sum")
        text = text.substitute(balance=self.__Lang.wallet.balance, wallet=await func.int_to_str(num=self.__data.get('wallet')),
                               sum=self.__Lang.wallet.sum)
        return text

    async def menu_payment(self):
        text = Template("<b>$amount:</b> $cash $sum $nds\n"
                        "<b>$method:</b> $method_type\n\n"
                        "$press_button")
        text = text.substitute(amount=self.__Lang.wallet.payment,
                               cash=await func.int_to_str(num=(int(self.__data.get('cash') * nds))),
                               nds=self.__Lang.wallet.payment_start.nds,
                               method=self.__Lang.wallet.method, method_type=self.__data.get('method'),
                               sum=self.__Lang.wallet.sum, press_button=self.__Lang.wallet.press_button)
        return text

    async def menu_payment2(self):
        text = Template("<b>$amount:</b> $cash $sum $nds\n"
                        "<b>$method:</b> $method_type\n\n"
                        "$press_button")
        text = text.substitute(amount=self.__Lang.wallet.payment,
                               cash=await func.int_to_str(num=(int(self.__cash * nds))),
                               nds=self.__Lang.wallet.payment_start.nds,
                               method=self.__Lang.wallet.method, method_type=self.__data.get('method'),
                               sum=self.__Lang.wallet.sum, press_button=self.__Lang.wallet.press_button)
        return text

    async def menu_success(self):
        text = Template("$success <b>$cash $sum</b>")
        text = text.substitute(success=self.__Lang.wallet.success, sum=self.__Lang.wallet.sum,
                               cash=await func.int_to_str(num=self.__data.get('cash')))
        return text

    async def menu_withdraw_start(self):
        text = Template("<b>$balance:</b> $wallet $sum\n\n"
                        "$commission\n\n"
                        "$payDay")
        text = text.substitute(balance=self.__Lang.wallet.balance, sum=self.__Lang.wallet.sum,
                               wallet=await func.int_to_str(num=self.__data.get('wallet')),
                               commission=self.__Lang.wallet.commission,payDay=self.__Lang.wallet.payDay)
        return text

    async def menu_withdraw(self):
        text = Template("<b>$balance:</b> $cash $sum\n\n"
                        "$information")
        text = text.substitute(balance=self.__Lang.wallet.balance, cash=await func.int_to_str(num=self.__data.get('wallet')),
                               sum=self.__Lang.wallet.sum, information=self.__Lang.wallet.withdraw)
        return text

    async def menu_end(self, type_legal: str):
        if type_legal == "entity":
            type_legal = self.__Lang.wallet.entity
        elif type_legal == "individual":
            type_legal = self.__Lang.wallet.individual
        elif type_legal == "selfEmployedCard":
            type_legal = self.__Lang.wallet.selfEmployedCard
        elif type_legal == "selfEmployedAccount":
            type_legal = self.__Lang.wallet.selfEmployedAccount
        text = Template("$payDay\n"
                        "<b>$method:</b> $type_legal\n"
                        "<b>$credit:</b> $cash $sum")
        text = text.substitute(payDay=self.__Lang.wallet.payDay, method=self.__Lang.wallet.method,
                               type_legal=type_legal, credit=self.__Lang.wallet.credit,
                               cash=await func.int_to_str(num=ceil(self.__cash * bot_commission)),
                               sum=self.__Lang.wallet.sum)
        return text

    async def menu_deposit(self):
        text = Template("<b>$deposit</b>\n\n"
                        "<b>$method:</b> $method_user\n"
                        "<b>$cash:</b> $cash_user $sum\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$status:</b> $completed")
        text = text.substitute(deposit=self.__Lang.wallet.history.deposit,
                               method=self.__Lang.wallet.history.method,
                               method_user=self.__Lang.wallet.history.method_user,
                               cash=self.__Lang.wallet.history.cash,
                               cash_user=self.__Lang.wallet.history.cash_user,
                               sum=self.__Lang.wallet.history.sum,
                               date=self.__Lang.wallet.history.date,
                               date_user=self.__Lang.wallet.history.date_user,
                               status=self.__Lang.wallet.history.status,
                               completed=self.__Lang.wallet.history.completed)
        return text

    async def menu_write_off(self):
        text = Template("<b>$writeOff</b>\n\n"
                        "<b>$platform:</b> $url\n"
                        "<b>$cash:</b> $cash_user $sum\n"
                        "<b>$date:</b> $date_user\n"
                        "<b>$status:</b> $completed")
        text = text.substitute(deposit=self.__Lang.wallet.history.writeOff,
                               platform=self.__Lang.wallet.history.platform,
                               url=self.__Lang.wallet.history.method_user,
                               cash=self.__Lang.wallet.history.cash,
                               cash_user=self.__Lang.wallet.history.cash_user,
                               sum=self.__Lang.wallet.history.sum,
                               date=self.__Lang.wallet.history.date,
                               date_user=self.__Lang.wallet.history.date_user,
                               status=self.__Lang.wallet.history.status,
                               completed=self.__Lang.wallet.history.completed)
        return text

    async def menu_success_campaign(self, cash: int):
        text = Template("$success\n"
                        "<b>$wallet $cost $sum</b>\n"
                        "$payment")
        text = text.substitute(success=self.__Lang.formOrder.payment.success,
                               wallet=self.__Lang.formOrder.payment.wallet,
                               cost=await func.int_to_str(num=cash),
                               sum=self.__Lang.formOrder.payment.sum,
                               payment=self.__Lang.formOrder.payment.payment)
        return text

    async def menu_payment_campaign(self):
        text = Template("<b>$fail</b>\n\n"
                        "$count <b>$cost $sum</b>👇")
        text = text.substitute(fail=self.__Lang.formOrder.payment.fail, count=self.__Lang.formOrder.payment.count,
                               cost=await func.int_to_str(num=int(self.__payment)), sum=self.__Lang.formOrder.payment.sum)
        return text

    async def menu_history(self):
        await self._check_type_legal()
        return await self._get_type()

    async def _get_type(self):
        if self.__data.get("method") == "deposit":
            return await self._deposit()
        elif self.__data.get("method") == "withdrawal":
            await self._check_status()
            return await self._withdraw()
        elif self.__data.get("method") == "write_off":
            return await self._write_off()
        elif self.__data.get("method") == "reject":
            return await self._reject()
        elif self.__data.get("method") == "complete":
            return await self._complete()

    async def _check_type_legal(self):
        if self.__data.get("type_legal") == "entity":
            self.__type_legal = self.__Lang.wallet.entity
        elif self.__data.get("type_legal") == "individual":
            self.__type_legal = self.__Lang.wallet.individual
        elif self.__data.get("type_legal") == "self_employed":
            self.__type_legal = self.__Lang.wallet.selfEmployedAccount
        elif self.__data.get("type_legal") == "self_employed_transit":
            self.__type_legal = self.__Lang.wallet.selfEmployedCard
        elif self.__data.get("type_legal") == "click":
            self.__type_legal = "Click"
        elif self.__data.get("type_legal") == "payme":
            self.__type_legal = "Payme"

    async def _check_status(self):
        self.__reason = ""
        if self.__data.get("status") == 1:
            self.__status = self.__Lang.wallet.history.completed
        elif self.__data.get("status") == -1:
            self.__status = self.__Lang.wallet.history.rejected
            text = Template("<b>$reason:</b> $event_reason")
            self.__reason = text.substitute(reason=self.__Lang.wallet.history.reason,event_reason=self.__data.get("reason"))
        elif self.__data.get("status") == 0:
            self.__status = self.__Lang.wallet.history.expects

    async def _withdraw(self):
        text = Template("$withdraw\n\n"
                        "<b>$method</b>: $type_legal\n"
                        "<b>$cash:</b> $wallet $sum <i>$commission</i>\n"
                        "<b>$date:</b> $event_date\n"
                        "<b>$status:</b> $event_status\n"
                        "$reason")
        text = text.substitute(withdraw=self.__Lang.wallet.history.withdraw,
                               method=self.__Lang.wallet.history.method, type_legal=self.__type_legal,
                               cash=self.__Lang.wallet.history.cash,
                               wallet=await func.int_to_str(num=self.__data.get("wallet")),
                               sum=self.__Lang.wallet.history.sum, commission=self.__Lang.wallet.history.commission,
                               date=self.__Lang.wallet.history.date, event_date=self.__data.get("date"),
                               status=self.__Lang.wallet.history.status, event_status=self.__status,
                               reason=self.__reason)
        return text

    async def _deposit(self):
        text = Template("$deposit\n\n"
                        "<b>$method</b>: $type_legal\n"
                        "<b>$cash:</b> $wallet $sum\n"
                        "<b>$date:</b> $event_date\n"
                        "<b>$status:</b> $event_status\n")
        text = text.substitute(deposit=self.__Lang.wallet.history.deposit,
                               method=self.__Lang.wallet.history.method, type_legal=self.__type_legal,
                               cash=self.__Lang.wallet.history.cash,
                               wallet=await func.int_to_str(num=self.__data.get("wallet")),
                               sum=self.__Lang.wallet.history.sum,
                               date=self.__Lang.wallet.history.date, event_date=self.__data.get("date"),
                               status=self.__Lang.wallet.history.status,
                               event_status=self.__Lang.wallet.history.completed)
        return text

    async def _write_off(self):
        text = Template("$write_off\n\n"
                        "<b>$campaign</b>: $campaign_name\n"
                        "<b>$cash:</b> $wallet $sum\n"
                        "<b>$date:</b> $event_date\n"
                        "<b>$status:</b> $event_status\n")
        text = text.substitute(write_off=self.__Lang.wallet.history.writeOff,
                               campaign=self.__Lang.wallet.history.campaign,
                               campaign_name=hlink(url=self.__data.get("url"), title=self.__data.get("name")),
                               cash=self.__Lang.wallet.history.cash,
                               wallet=await func.int_to_str(num=self.__data.get("wallet")),
                               sum=self.__Lang.wallet.history.sum,
                               date=self.__Lang.wallet.history.date, event_date=self.__data.get("date"),
                               status=self.__Lang.wallet.history.status,
                               event_status=self.__Lang.wallet.history.completed)
        return text

    async def _reject(self):
        platform = "" if self.__data.get("url") is None else f'<b>{self.__Lang.wallet.history.platform}:</b> {hlink(url=self.__data.get("url"), title=self.__data.get("area_name"))}\n'
        text = Template("$reject\n\n"
                        "$platform"
                        "<b>$cash:</b> $wallet $sum\n"
                        "<b>$date:</b> $event_date\n"
                        "<b>$status:</b> $event_status\n")
        text = text.substitute(reject=self.__Lang.wallet.history.reject,
                               cash=self.__Lang.wallet.history.cash,
                               platform=platform,
                               wallet=await func.int_to_str(num=self.__data.get("wallet")),
                               sum=self.__Lang.wallet.history.sum,
                               date=self.__Lang.wallet.history.date, event_date=self.__data.get("date"),
                               status=self.__Lang.wallet.history.status,
                               event_status=self.__Lang.wallet.history.completed)
        return text

    async def _complete(self):
        text = Template("$complete\n\n"
                        "<b>$platform</b>: $platform_name\n"
                        "<b>$cash:</b> $wallet $sum\n"
                        "<b>$date:</b> $event_date\n"
                        "<b>$status:</b> $event_status\n")
        text = text.substitute(complete=self.__Lang.wallet.history.complete,
                               platform=self.__Lang.wallet.history.platform,
                               platform_name=hlink(url=self.__data.get("url"), title=self.__data.get("area_name")),
                               cash=self.__Lang.wallet.history.cash,
                               wallet=await func.int_to_str(num=self.__data.get("wallet")),
                               sum=self.__Lang.wallet.history.sum,
                               date=self.__Lang.wallet.history.date, event_date=self.__data.get("date"),
                               status=self.__Lang.wallet.history.status,
                               event_status=self.__Lang.wallet.history.completed)
        return text





