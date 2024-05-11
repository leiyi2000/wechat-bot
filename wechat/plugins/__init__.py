from wechat.command import CommandRouter
from wechat.plugins import setu, weather, epic


router = CommandRouter()
router.include_router(setu.router)
router.include_router(weather.router)
router.include_router(epic.router)
