from text.language.ru import Ru_language
from text.language.eng import Eng_language
from text.language.ozb import Ozb_language

RU = Ru_language()
OZB = Ru_language()
ENG = Ru_language()
# OZB = Ru_language()
# ENG = Eng_language()


class Text_main:

    choose_language = f"🇺🇿 Tilni tanlang 👇\n" \
                      f"🇷🇺 Выберите язык 👇\n" \
                      f"🇺🇸 Choose language 👇\n"

    language = {"rus": RU, "ozb": OZB, "eng": ENG}

    start_text = "Какой-то текст с объяснением что за" \
            "\nсервис, плюсы минусы и тд" \
            "\nПример:" \
            "\nVenkon Digital — помогаем брендам и компаниям" \
            "\nтранслировать свои маркетинговые активности" \
            "\nчерез лидеров мнений и блогеров" \
            "\nНам доверяют (компании):" \
            "\n1. далыодла" \
            "\n2. адлподва" \
            "\n3. адлподал" \
            "\nС нами сотрудничают (блогеры):" \
            "\n1. авпвап" \
            "\n2. авпвап" \
            "\n3. авлдопалд"

    class settings:
        rus = "🇷🇺 Ru"
        ozb = "🇺🇿 O’z"
        eng = "🇺🇸 Eng"
        language = [rus, ozb, eng]

    class start:
        blogger = [RU.start.blogger, OZB.start.blogger, ENG.start.blogger]
        advertiser = [RU.start.advertiser, OZB.start.advertiser, ENG.start.advertiser]
        start = [RU.buttons.common.start, OZB.buttons.common.start, ENG.buttons.common.start]

    class menu:
        menu = [RU.menu.blogger.menu, OZB.menu.blogger.menu, ENG.menu.blogger.menu]
        platform = [RU.menu.blogger.platform, OZB.menu.blogger.platform, ENG.menu.blogger.platform]
        activeOrder = [RU.menu.blogger.activeOrder, OZB.menu.blogger.activeOrder, ENG.menu.blogger.activeOrder]
        account = [RU.menu.blogger.account, OZB.menu.blogger.account, ENG.menu.blogger.account]
        wallet = [RU.menu.blogger.wallet, OZB.menu.blogger.wallet, ENG.menu.blogger.wallet]
        information = [RU.menu.blogger.information, OZB.menu.blogger.information, ENG.menu.blogger.information]
        lang = [RU.menu.blogger.lang, OZB.menu.blogger.lang, ENG.menu.blogger.lang]
        change_blogger = [RU.menu.blogger.change, OZB.menu.blogger.change, ENG.menu.blogger.change]
        change_advertiser = [RU.menu.advertiser.change, OZB.menu.advertiser.change, ENG.menu.advertiser.change]
        formOrder = [RU.menu.advertiser.formOrder, OZB.menu.advertiser.formOrder, ENG.menu.advertiser.formOrder]
        basket = [RU.menu.advertiser.basket, OZB.menu.advertiser.basket, ENG.menu.advertiser.basket]
        nextTime = [RU.buttons.common.nextTime, OZB.buttons.common.nextTime, ENG.buttons.common.nextTime]
        task = [RU.buttons.common.task, OZB.buttons.common.task, ENG.buttons.common.task]
        logout = [RU.buttons.personalData.logoutAccount, OZB.buttons.personalData.logoutAccount, ENG.buttons.personalData.logoutAccount]

    class information:
        about_us = [RU.information.about_us, OZB.information.about_us, ENG.information.about_us]
        how_to_use = [RU.information.how_to_use, OZB.information.how_to_use, ENG.information.how_to_use]
        feedback = [RU.information.feedback, OZB.information.feedback, ENG.information.feedback]

    class common:
        skip = [RU.buttons.common.skip, OZB.buttons.common.skip, ENG.buttons.common.skip]
        nextTime = [RU.buttons.common.nextTime, OZB.buttons.common.nextTime, ENG.buttons.common.nextTime]
        confirm = [RU.buttons.common.accept, OZB.buttons.common.accept, ENG.buttons.common.accept]

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





