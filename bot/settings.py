import os

from datetime import tzinfo, timedelta


APP_NAME = "bot"
WX_BOT_API = os.environ["WX_BOT_API"]
WX_BOT_API_V1 = WX_BOT_API.replace("/v2", "")
DATABASE_URL = os.environ.get("DATABASE_URL", default="sqlite://bot.sqlite3")
TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "./plugins/template",
)


# 数据量配置
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        APP_NAME: {
            "models": ["bot.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Shanghai",
}


class ShanghaiTZ(tzinfo):
    def __init__(self):
        self._offset = timedelta(hours=8)
        self._name = "Asia/Shanghai"

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return timedelta(0)


# 上海时区
SHANGHAI_TIMEZONE = ShanghaiTZ()
