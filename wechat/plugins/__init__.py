from wechat.schedule import Schedule
from wechat.command import CommandRouter
from wechat.plugins import (
    bilibili,
    setu,
    weather,
    epic,
    kfc,
    lol,
    news,
    leetcode,
)


# 指令注入
router = CommandRouter()
router.include_router(lol.router)
router.include_router(kfc.router)
router.include_router(setu.router)
router.include_router(epic.router)
router.include_router(weather.router)
router.include_router(bilibili.router)
router.include_router(news.router)
router.include_router(leetcode.router)


# 定时任务
schedule = Schedule()
