from enum import StrEnum

import structlog

from wechat.models import Config as ConfigModel


log = structlog.get_logger()


class ConfigKey(StrEnum):
    lol_wegame_cookie = "lol_wegame_cookie"
    error_reply = "error_reply"
    weather_api_key = "weather_api_key"


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
