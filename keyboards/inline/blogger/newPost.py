from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.language.main import Text_main

Txt = Text_main()


class InlinePostBlogger():

    def __init__(self, language: str, order_id: int = None,  client_id: int = None, blogger_area_id: int = None,
                 area_id: int = None):
        self.__markup = None
        self.__order_id = order_id
        self.__client_id = client_id
        self.__blogger_area_id = blogger_area_id
        self.__area_id = area_id
        self.__Lang = Txt.language[language]

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Lang.buttons.newPost.cancel, callback_data=f"Reject_{self.__blogger_area_id}")
        back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"RejectBack_{self.__blogger_area_id}")
        markup.add(b, back)
        return markup

    async def menu_new_post(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.newPost.accept,
                                  callback_data=f"NewAccept_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.newPost.checkPost,
                                  callback_data=f"CheckPost_{self.__order_id}")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.newPost.reject,
                                  callback_data=f"NewReject_{self.__blogger_area_id}")
        markup.add(b1, b2, b3)
        return markup

    async def menu_accept(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.check, callback_data=f"PostPost_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"CheckPost_{self.__order_id}")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.post.advertiser, callback_data=f"MessageFromAdvertiser_{self.__blogger_area_id}")
        b4 = InlineKeyboardButton(text=self.__Lang.buttons.post.cancel, callback_data=f"PostCancel_{self.__blogger_area_id}")
        markup.add(b1, b2, b3, b4)
        return markup

    async def menu_back2(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Lang.buttons.newPost.cancel, callback_data=f"Reject_{self.__blogger_area_id}")
        back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"PostBack_{self.__blogger_area_id}")
        markup.add(b, back)
        return markup

    async def menu_back3(self):
        markup = InlineKeyboardMarkup(row_width=1)
        back = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"PostBack_{self.__blogger_area_id}")
        markup.add(back)
        return markup

    async def menu_send_advertiser(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.blogger,
                                  callback_data=f"NewMessageFromBlogger_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"CheckPost_{self.__order_id}")
        markup.add(b1, b2)
        return markup

    async def menu_back_send_advertiser(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.back,
                                  callback_data=f"BackNewMessageFromBlogger_{self.__blogger_area_id}")
        markup.add(b1)
        return markup

    async def menu_send_blogger(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.advertiser,
                                  callback_data=f"NewMessageFromAdvertiser_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"CheckPost_{self.__order_id}")
        markup.add(b1, b2)
        return markup

    async def menu_back_send_blogger(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.back,
                                  callback_data=f"BackNewMessageFromAdvertiser_{self.__blogger_area_id}")
        markup.add(b1)
        return markup

    async def menu_back_send_blogger2(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.common.back,
                                  callback_data=f"BackMessageFromAdvertiser_{self.__blogger_area_id}")
        markup.add(b1)
        return markup

    async def menu_accept_post(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.accept, callback_data=f"PostAdvertiserAccept_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"CheckPost_{self.__order_id}")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.post.reject, callback_data=f"PostAdvertiserReject_{self.__blogger_area_id}")
        markup.add(b1, b2, b3)
        return markup

    async def menu_back_accept_post(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.moderation, callback_data=f"ModerationPostAdvertiser_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.common.back, callback_data=f"BackPostAdvertiser_{self.__blogger_area_id}")
        markup.add(b1, b2)
        return markup

    async def menu_moderation_post(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.toBlogger, callback_data=f"FavorPostBlogger_{self.__blogger_area_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.toAdvertiser, callback_data=f"FavorPostAdvertiser_{self.__blogger_area_id}")
        b3 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"FavorCheckPost_{self.__order_id}")
        markup.add(b1, b2, b3)
        return markup

    async def menu_check_post(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"CheckPost_{self.__order_id}")
        markup.add(b1)
        return markup

    async def menu_check_post2(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.post, callback_data=f"CheckPost_{self.__order_id}")
        b2 = InlineKeyboardButton(text=self.__Lang.buttons.post.blogger, callback_data=f"NewMessageFromBlogger_{self.__blogger_area_id}")
        markup.add(b1, b2)
        return markup

    async def menu_rate_post(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Lang.buttons.post.rate, callback_data=f"RatePost_{self.__area_id}")
        markup.add(b1)
        return markup

    async def menu_rate(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data=f"RatePoint_5_{self.__area_id}")
        b2 = InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data=f"RatePoint_4_{self.__area_id}")
        b3 = InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"RatePoint_3_{self.__area_id}")
        b4 = InlineKeyboardButton(text="⭐⭐", callback_data=f"RatePoint_2_{self.__area_id}")
        b5 = InlineKeyboardButton(text="⭐", callback_data=f"RatePoint_1_{self.__area_id}")
        markup.add(b1, b2, b3, b4, b5)
        return markup

