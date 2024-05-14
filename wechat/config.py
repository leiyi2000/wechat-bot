import structlog

from wechat.models import Config as ConfigModel


log = structlog.get_logger()


class ConfigKey:
    """配置KEY"""

    kfc_api = "kfc_api"
    setu_api = "setu_api"
    error_reply = "error_reply"
    news_api_key = "news_api_key"
    weather_api_key = "weather_api_key"


class Config:
    """配置"""

    async def _find(self, key: str, default: str | None = None) -> str | None:
        config = await ConfigModel.get_or_none(key=key)
        if config is None:
            log.warning(f"config {key} not set")
            return default
        else:
            return config.value

    async def lol_wegame_cookie(self) -> str:
        return await self._find(ConfigKey.lol_wegame_cookie)

    async def error_reply(self) -> str:
        return await self._find(ConfigKey.error_reply, default="哼哼~~, 才不是我的问题!")

    async def weather_api_key(self) -> str:
        return await self._find(ConfigKey.weather_api_key, default="")

    async def setu_api(self) -> str:
        return await self._find(ConfigKey.setu_api, default="https://api.anosu.top/img?$alias=cloud.jpg")

    async def kfc_api(self) -> str:
        return await self._find(ConfigKey.kfc_api, default="https://api.jixs.cc/api/wenan-fkxqs/index.php")

    async def news_api_key(self) -> str:
        return await self._find(ConfigKey.news_api_key, default="")


config = Config()
