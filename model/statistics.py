from typing import TypedDict


class PeriodModel(TypedDict, total=False):
    period: int
    for_all: int


class WithdrawModel(TypedDict, total=False):
    withdrawal_amount: PeriodModel
    entity: PeriodModel
    self_employed: PeriodModel
    withdrawal_count_success: PeriodModel
    withdrawal_count_rejected: PeriodModel


class DepositModel(TypedDict, total=False):
    completed_amount: PeriodModel
    entity_or_individual: PeriodModel
    self_employed: PeriodModel
    payme: PeriodModel
    click: PeriodModel
    completed_count: PeriodModel


class BalanceModel(TypedDict, total=False):
    deposit: DepositModel
    withdrawal: WithdrawModel


class OrdersModel(TypedDict, total=False):
    complete: PeriodModel
    rejected_by_blogger: PeriodModel
    rejected_by_advertiser: PeriodModel
    canceled_by_blogger: PeriodModel


class CampaignModel(TypedDict, total=False):
    new: PeriodModel
    active_now: int
    max_areas_per_campaign: int
    min_areas_per_campaign: int


class AreasModel(TypedDict, total=False):
    active: PeriodModel
    moderation: PeriodModel
    rejected_by_moderation: PeriodModel
    deleted_by_blogger: PeriodModel
    banned: PeriodModel
    telegram: PeriodModel
    youtube: PeriodModel
    instagram: PeriodModel


class UsersModel(TypedDict, total=False):
    active_users: PeriodModel
    blocked_users: int
    bloggers: PeriodModel
    advertisers: PeriodModel


class CurrentPeriodModel(TypedDict, total=False):
    from_date: str
    until_date: str


class StatisticsModel(TypedDict, total=False):
    current_period: CurrentPeriodModel
    users: UsersModel
    areas: AreasModel
    campaigns: CampaignModel
    blogger_orders: OrdersModel
    balance: BalanceModel



