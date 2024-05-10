"""任务执行"""
import asyncio
from functools import partial

import httpx
import structlog

from wechat.plugins import router
from wechat.settings import WX_BOT_API
from wechat.schemas import Event as EventSchema


log = structlog.get_logger()


async def event_task(event: EventSchema):
    routes = router.matches(event)
    for route in routes:
        func = route.func
        # 判断是否需要传入事件对象
        if route.event_arg:
            func = partial(func, event)
        if asyncio.iscoroutinefunction(func):
            reply = await func(**route.func_kwargs)
        else:
            reply = func(**route.func_kwargs)
        if reply:
            async with httpx.AsyncClient() as client:
                await client.post(WX_BOT_API, json=reply.model_dump(by_alias=True))

# TODO ylei 定时任务
