from text.language.ru import Ru_language
from text.language.uzb import Uzb_language

RU = Ru_language()
UZB = Uzb_language()
ENG = Ru_language()


class Text_main:

    choose_language = f"🇺🇿 Тилни танланг 👇\n" \
                      f"🇷🇺 Выберите язык 👇\n"

    rus_var = "rus"
    uzb_var = "uzb"
    eng_var = "eng"

    language = {rus_var: RU, uzb_var: UZB, eng_var: ENG}

    class settings:
        rus = "🇷🇺 Ru"
        uzb = "🇺🇿 O’z"
        language = [rus, uzb]

    class start:
        blogger = [RU.start.blogger, UZB.start.blogger, ENG.start.blogger]
        advertiser = [RU.start.advertiser, UZB.start.advertiser, ENG.start.advertiser]
        start = [RU.buttons.common.start, UZB.buttons.common.start, ENG.buttons.common.start]

    class menu:
        menu = [RU.menu.blogger.menu, UZB.menu.blogger.menu, ENG.menu.blogger.menu]
        platform = [RU.menu.blogger.platform, UZB.menu.blogger.platform, ENG.menu.blogger.platform]
        activeOrder = [RU.menu.blogger.activeOrder, UZB.menu.blogger.activeOrder, ENG.menu.blogger.activeOrder]
        account = [RU.menu.blogger.account, UZB.menu.blogger.account, ENG.menu.blogger.account]
        wallet = [RU.menu.blogger.wallet, UZB.menu.blogger.wallet, ENG.menu.blogger.wallet]
        information = [RU.menu.blogger.information, UZB.menu.blogger.information, ENG.menu.blogger.information]
        lang = [RU.menu.blogger.lang, UZB.menu.blogger.lang, ENG.menu.blogger.lang]
        change_blogger = [RU.menu.blogger.change, UZB.menu.blogger.change, ENG.menu.blogger.change]
        change_advertiser = [RU.menu.advertiser.change, UZB.menu.advertiser.change, ENG.menu.advertiser.change]
        formOrder = [RU.menu.advertiser.formOrder, UZB.menu.advertiser.formOrder, ENG.menu.advertiser.formOrder]
        basket = [RU.menu.advertiser.basket, UZB.menu.advertiser.basket, ENG.menu.advertiser.basket]
        nextTime = [RU.buttons.common.nextTime, UZB.buttons.common.nextTime, ENG.buttons.common.nextTime]
        task = [RU.buttons.common.task, UZB.buttons.common.task, ENG.buttons.common.task]
        logout = [RU.buttons.personalData.logoutAccount, UZB.buttons.personalData.logoutAccount, ENG.buttons.personalData.logoutAccount]

    class information:
        about_us = [RU.information.about_us, UZB.information.about_us, ENG.information.about_us]
        how_to_use = [RU.information.how_to_use, UZB.information.how_to_use, ENG.information.how_to_use]
        feedback = [RU.information.feedback, UZB.information.feedback, ENG.information.feedback]

    class common:
        skip = [RU.buttons.common.skip, UZB.buttons.common.skip, ENG.buttons.common.skip]
        nextTime = [RU.buttons.common.nextTime, UZB.buttons.common.nextTime, ENG.buttons.common.nextTime]
        confirm = [RU.buttons.common.accept, UZB.buttons.common.accept, ENG.buttons.common.accept]

    class commission:
        nds = 12
        bot = 3
        min_payment = 30000


    class group:
        moderation = "💬 Площадки на модерации"
        withdraw = "💵 Заявки на вывод средств"
        banPlatform = "⛔ Забанить/Разбанить площадку"

    class limit:
        class blogger:
            allPlatform = 10
            allOrders = 10
            orders = 10

        class advertiser:
            formOrder = 30
            orders = 10
            basket = 40

    # class personal_cabinet:
    #     data = [RU.buttons.personal_cabinet.data.data, UZB.buttons.personal_cabinet.data.data,
    #             OZB.buttons.personal_cabinet.data.data]
    #     wallet = [RU.buttons.personal_cabinet.wallet.wallet, UZB.buttons.personal_cabinet.wallet.wallet,
    #               OZB.buttons.personal_cabinet.wallet.wallet]





