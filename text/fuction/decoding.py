from looping import fastapi
from model.platform import GetValue
from text.language.main import Text_main

Txt = Text_main()


class Decoding:

    def __init__(self, language: str, token: str, param_id: [int, list] = None):
        self.__language = language
        self.__token = token
        self.__param_id = param_id

    async def get_category(self):
        params = GetValue(language=self.__language, category_id=self.__param_id)
        json = await fastapi.get_channel_category(params=params, token=self.__token)
        return json.get("name")

    async def get_sex(self):
        params = GetValue(language=self.__language, ratio_id=self.__param_id)
        json = await fastapi.get_channel_sex_ratio(params=params, token=self.__token)
        return json.get("name")

    async def get_age(self):
        params = GetValue(language=self.__language, age_id=self.__param_id)
        json = await fastapi.get_channel_age_ratio(params=params, token=self.__token)
        return json.get("name")

    async def get_lang(self):
        languages = []
        for lang_id in self.__param_id:
            params = GetValue(language=self.__language, lang_id=lang_id)
            json = await fastapi.get_channel_language(params=params, token=self.__token)
            languages.append(json.get("name"))
        return languages
        # self.__lang_platform = str(', '.join((lang for lang in languages)))

    async def get_region(self):
        params = GetValue(language=self.__language, region_id=self.__param_id)
        json = await fastapi.get_region(params=params, token=self.__token)
        return json.get("name")

    async def get_platform(self):
        params = GetValue(language=self.__language, channel_id=self.__param_id)
        json = await fastapi.get_channel_type(params=params, token=self.__token)
        return json.get("name")

