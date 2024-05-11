import os


WX_BOT_API = os.environ.get("WX_BOT_API")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
ERROR_REPLY = os.environ.get("ERROR_REPLY", default="哼, 出错了!")