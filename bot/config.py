import json

import structlog

from bot.models import Config as ConfigModel


log = structlog.get_logger()


class Undefined:
    pass


undefined = Undefined()


class Kfc:
    def __init__(self) -> None:
        self.api: str | Undefined = undefined
        self.name = "kfc"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is None:
            value = "https://api.jixs.cc/api/wenan-fkxqs/index.php"
        else:
            value = config.value
        self.load(value)

    def load(self, value: str):
        self.api = value


class News:
    def __init__(self) -> None:
        self.api_key: str | Undefined = undefined
        self.name = "news"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is not None:
            self.load(config.value)
        else:
            log.warning(f"config {self.name} not set")

    def load(self, value: str):
        self.api_key = value


class Setu:
    def __init__(self) -> None:
        self.api: str | Undefined = undefined
        self.name = "setu"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is None:
            value = "https://api.anosu.top/img?$alias=cloud.jpg"
        else:
            value = config.value
        self.load(value)

    def load(self, value: str):
        self.api = value


class AList:
    def __init__(self) -> None:
        self.api: str | Undefined = undefined
        self.api_key: str | Undefined = undefined
        self.path: str | Undefined = undefined
        self.enable: bool = False
        self.name = "alist"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is not None:
            self.load(config.value)
        else:
            log.warning(f"config {self.name} not set")

    def load(self, value: str):
        self.enable = True
        value = json.loads(value)
        self.api = value["api"]
        self.api_key = value["api_key"]
        self.path = value["path"]


class Wegame:
    def __init__(self) -> None:
        self.cookie: str | Undefined = undefined
        self.name = "wegame"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is not None:
            self.load(config.value)
        else:
            log.warning(f"config {self.name} not set")

    def load(self, value: str):
        self.cookie = value


class Weather:
    def __init__(self) -> None:
        self.amap_key: str | Undefined = undefined
        self.name = "weather"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is not None:
            self.load(config.value)
        else:
            log.warning(f"config {self.name} not set")

    def load(self, value: str):
        self.amap_key = value


class Error:
    def __init__(self) -> None:
        self.reply: str | Undefined = undefined
        self.name = "error"

    async def load_from_db(self) -> None:
        config = await ConfigModel.get_or_none(key=self.name)
        if config is None:
            value = "哼哼~~, 才不是我的问题!"
        else:
            value = config.value
        self.load(value)

    def load(self, value: str):
        self.reply = value


class Config:
    def __init__(self) -> None:
        self.kfc = Kfc()
        self.news = News()
        self.setu = Setu()
        self.alist = AList()
        self.wegame = Wegame()
        self.weather = Weather()
        self.error = Error()
        # 通过key匹配对应的配置管理
        self._map = {}

    async def load_from_db(self):
        await self.kfc.load_from_db()
        await self.news.load_from_db()
        await self.setu.load_from_db()
        await self.alist.load_from_db()
        await self.wegame.load_from_db()
        await self.weather.load_from_db()
        await self.error.load_from_db()
        self._map[self.kfc.name] = self.kfc
        self._map[self.news.name] = self.news
        self._map[self.setu.name] = self.setu
        self._map[self.alist.name] = self.alist
        self._map[self.wegame.name] = self.wegame
        self._map[self.weather.name] = self.weather
        self._map[self.error.name] = self.error

    def load(self, key: str, value: str):
        if key in self._map:
            self._map[key].load(value)


config = Config()
