import os


APP_NAME = "wechat"
WX_BOT_API = os.environ.get("WX_BOT_API")
WX_BOT_API_V1 = WX_BOT_API.replace("/v2", "")
DATABASE_URL = os.environ.get("DATABASE_URL", default="sqlite://wechat.sqlite3")
TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 
    "./plugins/template",
)


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
