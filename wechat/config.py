import structlog

from wechat.models import Config as ConfigModel


log = structlog.get_logger()


class ConfigKey:
    kfc_api = "kfc_api"
    setu_api = "setu_api"
    error_reply = "error_reply"
    weather_api_key = "weather_api_key"
    lol_wegame_cookie = "lol_wegame_cookie"
    news_api_key = "news_api_key"


async def lol_wegame_cookie() -> str:
    config = await ConfigModel.get_or_none(key=ConfigKey.lol_wegame_cookie)
    if config is None:
        log.warning("lol_wegame_cookie is not set")
        return ""
    else:
        return config.value


async def error_reply() -> str:
    config = await ConfigModel.get_or_none(key=ConfigKey.error_reply)
    if config is None:
        return "哼哼~~, 才不是我的问题!"
    else:
        return config.value


async def weather_api_key() -> str:
    config = await ConfigModel.get_or_none(key=ConfigKey.weather_api_key)
    if config is None:
        log.warning("weather_api_key is not set")
        return ""
    else:
        return config.value


async def setu_api() -> str:
    config = await ConfigModel.get_or_none(key=ConfigKey.setu_api)
    if config is None:
        log.warning("setu_api is not set")
        return "https://api.anosu.top/img?$alias=cloud.jpg"
    else:
        return config.value


async def kfc_api() -> str:
    config = await ConfigModel.get_or_none(key=ConfigKey.kfc_api)
    if config is None:
        log.warning("kfc_api is not set")
        return "https://api.jixs.cc/api/wenan-fkxqs/index.php"
    else:
        return config.value


async def news_api_key() -> str:
    config = await ConfigModel.get_or_none(key=ConfigKey.news_api_key)
    if config is None:
        log.warning("news_api_key is not set")
        return ""
    else:
        return config.value
