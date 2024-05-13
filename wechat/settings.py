import os


APP_NAME = "wechat"
WX_BOT_API = os.environ.get("WX_BOT_API")
DATABASE_URL = os.environ.get("DATABASE_URL", default="sqlite://wechat.sqlite3")


# 数据量配置
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        APP_NAME: {
            "models": ["wechat.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Shanghai",
}
