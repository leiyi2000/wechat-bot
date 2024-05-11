from wechat.command import CommandRouter
from wechat.plugins import (
    setu, 
    weather, 
    epic, 
    kfc,
)


router = CommandRouter()
# 指令注入
router.include_router(kfc.router)
router.include_router(setu.router)
router.include_router(epic.router)
router.include_router(weather.router)

