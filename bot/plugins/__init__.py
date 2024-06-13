from bot.command import CommandRouter
from bot.plugins import (
    bilibili,
    setu,
    weather,
    epic,
    kfc,
    news,
    leetcode,
)


# 指令注入
router = CommandRouter()
router.include_router(kfc.router)
router.include_router(setu.router)
router.include_router(epic.router)
router.include_router(weather.router)
router.include_router(bilibili.router)
router.include_router(news.router)
router.include_router(leetcode.router)
