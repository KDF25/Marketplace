from string import Template
from looping import pg, fastapi
from model.statistics import StatisticsModel
from text.language.main import Text_main

Txt = Text_main()


class FormAdmin:

    @staticmethod
    async def mail_end():
        count = await pg.get_all_unblock()
        text = Template('Рассылка завершена.\n'
                        'Доставлено — $nonblock пользователям.\n'
                        'Бот заблокирован — $block пользователями')
        text = text.substitute(nonblock=count[0][0], block=count[1][0])
        return text

    @staticmethod
    async def menu_statistics(json: dict):
        statistics: StatisticsModel = await fastapi.statistics(json=json)
        text = Template("<b>Сводка: $from_date - $until_date</b>\n\n"                        
                        "<b>👥 Пользователи:</b>\n"
                        "• активные пользователи (новые/общее) - $active_users_period/$active_users_for_all\n"
                        "• заблокированные - $blocked_users\n\n"
                        "• блогеры (новые/общее) - $bloggers_period/$bloggers_for_all\n"
                        "• рекламодатели (новые/общее) - $advertiser_period/$advertiser_for_all\n\n"
                        "———————————————\n\n"
                        "<b>💬 Площадки:</b>\n"
                        "• активные (новые/общее) - $areas_active_period/$areas_active_for_all\n"
                        "• на модерации - $areas_moderation\n"
                        "• отклонены модерацией (новые/общее) - $rejected_by_moderation_period/$rejected_by_moderation_for_all\n"
                        "• удаленные блогером (новые/общее) - $deleted_by_blogger_period/$deleted_by_blogger_for_all\n"
                        "• забаненные в группе (новые/общее) - $banned_period/$banned_for_all\n\n"
                        "• telegram (новые/общее) - $telegram_period/$telegram_for_all\n"
                        "• youtube (новые/общее) - $youtube_period/$youtube_for_all\n"
                        "• instagram (новые/общее) - $instagram_period/$instagram_for_all\n\n"
                        "———————————————\n\n"
                        "<b>🗓 Рекламные кампании:</b>"
                        "• Новые/Общее - $campaign_new_period/$campaign_new_for_all\n"
                        "• Активные сейчас - $campaign_active\n"
                        "• Максимальное количество площадок в одном заказе - $campaign_max\n"
                        "• Минимальное количество площадок в одном заказе - $campaign_min\n\n"
                        "———————————————\n\n"
                        "<b>🚀 Рекламные заказы</b>\n"
                        "• Выполненные (новые/общее) - $orders_period/$orders_for_all\n"
                        "• Отклонены блогером (новые/общее) - $orders_rejectedby_blogger_period/$orders_rejectedby_blogger_for_all\n"
                        "• Отклонены рекламодателем (новые/общее) - $orders_rejected_by_advertiser_period/$orders_rejected_by_advertiser_for_all\n"
                        "• Отменены блогером (новые/общее) - $orders_canceled_by_blogger_period/$orders_canceled_by_blogger_for_all\n\n"
                        "———————————————\n\n"
                        "<b>💵 Баланс</b>\n\n"
                        "<b>Пополнение:</b>\n"
                        "• Успешно пополнено (новое/общее) - $all_payment_period cум / $all_payment_for_all  сум\n"
                        "• Как юрлицо или ИП (новые/общее) - $entity_payment_period/$entity_payment_for_all\n\n"
                        "• Как самозанятый (новые/общее) - $self_employed_payment_period/$self_employed_payment_for_all\n"
                        "• Payme (новые/общее) - $payme_period/$payme_for_all\n"
                        "• Click (новые/общее) - $click_period/$click_for_all\n\n"
                        "• Количество успешных пополнений (новые/общее) - $payment_count_period/$payment_count_for_all\n\n"
                        "———————————————\n\n"
                        "<b>Вывод средств:</b>\n"
                        "• Успешно выведено (новое/общее) - $all_withdraw_period сум / $all_withdraw_for_all сум\n\n"
                        "• Как юрлицо или ИП (новые/общее) - $entity_withdraw_period/$entity_withdraw_for_all\n"
                        "• Как самозанятый (новые/общее) - $self_employed_withdraw_period/$self_employed_withdraw_for_all\n\n"
                        "• Успешный вывод (новые/общее) - $withdraw_count_period/$withdraw_count_for_all\n"
                        "• Отклоненный вывод (новые/общее) - $canceled_withdraw_count_period/$canceled_withdraw_count_for_all")
        text = text.substitute(
            from_date=statistics['current_period']['from_date'],
            until_date=statistics['current_period']['until_date'],
            active_users_period=statistics['users']['active_users']['period'],
            active_users_for_all=statistics['users']['active_users']['for_all'],
            blocked_users=statistics['users']['blocked_users'],
            bloggers_period=statistics['users']['bloggers']['period'],
            bloggers_for_all=statistics['users']['bloggers']['for_all'],
            advertiser_period=statistics['users']['advertisers']['period'],
            advertiser_for_all=statistics['users']['advertisers']['for_all'],
            areas_active_period=statistics['areas']['active']['period'],
            areas_active_for_all=statistics['areas']['active']['for_all'],
            areas_moderation=statistics['areas']['moderation'],
            rejected_by_moderation_period=statistics['areas']['rejected_by_moderation']['period'],
            rejected_by_moderation_for_all=statistics['areas']['rejected_by_moderation']['for_all'],
            deleted_by_blogger_period=statistics['areas']['deleted_by_blogger']['period'],
            deleted_by_blogger_for_all=statistics['areas']['deleted_by_blogger']['for_all'],
            banned_period=statistics['areas']['banned']['period'],
            banned_for_all=statistics['areas']['banned']['for_all'],
            telegram_period=statistics['areas']['telegram']['period'],
            telegram_for_all=statistics['areas']['telegram']['for_all'],
            youtube_period=statistics['areas']['youtube']['period'],
            youtube_for_all=statistics['areas']['youtube']['for_all'],
            instagram_period=statistics['areas']['instagram']['period'],
            instagram_for_all=statistics['areas']['instagram']['for_all'],
            campaign_new_period=statistics['campaigns']['new']['period'],
            campaign_new_for_all=statistics['campaigns']['new']['for_all'],
            campaign_active=statistics['campaigns']['active_now'],
            campaign_max=statistics['campaigns']['max_areas_per_campaign'],
            campaign_min=statistics['campaigns']['min_areas_per_campaign'],
            orders_period=statistics['blogger_orders']['complete']['period'],
            orders_for_all=statistics['blogger_orders']['complete']['for_all'],
            orders_rejectedby_blogger_period=statistics['blogger_orders']['rejected_by_blogger']['period'],
            orders_rejectedby_blogger_for_all=statistics['blogger_orders']['rejected_by_blogger']['for_all'],
            orders_rejected_by_advertiser_period=statistics['blogger_orders']['rejected_by_advertiser']['period'],
            orders_rejected_by_advertiser_for_all=statistics['blogger_orders']['rejected_by_advertiser']['for_all'],
            orders_canceled_by_blogger_period=statistics['blogger_orders']['canceled_by_blogger']['period'],
            orders_canceled_by_blogger_for_all=statistics['blogger_orders']['canceled_by_blogger']['for_all'],
            all_payment_period=statistics['balance']['deposit']['completed_amount']['period'],
            all_payment_for_all=statistics['balance']['deposit']['completed_amount']['for_all'],
            entity_payment_period=statistics['balance']['deposit']['entity_or_individual']['period'],
            entity_payment_for_all=statistics['balance']['deposit']['entity_or_individual']['for_all'],
            self_employed_payment_period=statistics['balance']['deposit']['self_employed']['period'],
            self_employed_payment_for_all=statistics['balance']['deposit']['self_employed']['for_all'],
            payme_period=statistics['balance']['deposit']['payme']['period'],
            payme_for_all=statistics['balance']['deposit']['payme']['for_all'],
            click_period=statistics['balance']['deposit']['click']['period'],
            click_for_all=statistics['balance']['deposit']['click']['for_all'],
            payment_count_period=statistics['balance']['deposit']['completed_count']['period'],
            payment_count_for_all=statistics['balance']['deposit']['completed_count']['for_all'],
            all_withdraw_period=statistics['balance']['withdrawal']['withdrawal_amount']['period'],
            all_withdraw_for_all=statistics['balance']['withdrawal']['withdrawal_amount']['for_all'],
            entity_withdraw_period=statistics['balance']['withdrawal']['entity']['period'],
            entity_withdraw_for_all=statistics['balance']['withdrawal']['entity']['for_all'],
            self_employed_withdraw_period=statistics['balance']['withdrawal']['self_employed']['period'],
            self_employed_withdraw_for_all=statistics['balance']['withdrawal']['self_employed']['for_all'],
            withdraw_count_period=statistics['balance']['withdrawal']['withdrawal_count_success']['period'],
            withdraw_count_for_all=statistics['balance']['withdrawal']['withdrawal_count_success']['for_all'],
            canceled_withdraw_count_period=statistics['balance']['withdrawal']['withdrawal_count_rejected']['period'],
            canceled_withdraw_count_for_all=statistics['balance']['withdrawal']['withdrawal_count_rejected']['for_all'],
        )
        return text
