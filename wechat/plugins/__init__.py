from wechat.command import CommandRouter
from wechat.plugins import setu


router = CommandRouter()
router.include_router(setu.router)
