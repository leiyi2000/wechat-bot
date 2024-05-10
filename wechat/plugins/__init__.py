from wechat.command import CommandRouter
from wechat.plugins import setu, weather


router = CommandRouter()
router.include_router(setu.router)
router.include_router(weather.router)
