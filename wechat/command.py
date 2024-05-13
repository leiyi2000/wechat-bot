from typing import Callable, Any, List, Dict

import asyncio
from functools import partial

import httpx
import structlog

from wechat import config
from wechat.settings import WX_BOT_API, WX_BOT_API_V1
from wechat.schemas import (
    Message,
    FileMessage,
    MessageType,
    ReplyMessage,
    Event as EventSchema,
)


log = structlog.get_logger()


class CommandRoute:
    """命令路由"""

    def __init__(
        self,
        name: str,
        prefix: str,
        func: Callable[..., Any],
        event_arg: bool,
        limit_room: bool,
        func_kwargs: Dict[str, Any],
    ) -> None:
        self.name = name
        self.prefix = prefix
        self.func = func
        self.event_arg = event_arg
        self.limit_room = limit_room
        self.func_kwargs = func_kwargs

    def match(self, event: EventSchema) -> bool:
        if self.limit_room and not event.is_room:
            return False
        return event.content.startswith(self.prefix)


class CommandRouter:
    """指令路由器"""

    def __init__(self):
        self.routes: List[CommandRoute] = []

    def add_route(self, route: CommandRoute):
        self.routes.append(route)

    def command(
        self,
        prefix: str,
        *,
        name: str = None,
        limit_room: bool = False,
        event_arg: bool = True,
        func_kwargs: Dict[str, Any] = {},
    ):
        """command装饰器

        Args:
            prefix (str): 指令前缀.
            func (Callable[..., Any]): 命令处理函数.
            name (str, optional): 名称.
            limit_room (bool, optional): True 限制只能处理群消息.
            event_arg (bool, optional): True 传递event参数到func.
            func_kwargs (Dict[str, Any], optional): func额外参数.
        """

        def decorator(func: Callable[..., Any]):
            # 初始化一个命令路由
            route = CommandRoute(
                name or func.__name__,
                prefix,
                func,
                event_arg,
                limit_room,
                func_kwargs,
            )
            self.add_route(route)
            return func

        return decorator

    def matches(self, event: EventSchema) -> List[CommandRoute]:
        return [route for route in self.routes if route.match(event)]

    def include_router(self, router: "CommandRouter"):
        for route in router.routes:
            self.add_route(route)


async def reply(
    event: EventSchema,
    reply_message: List[Message] | Message | FileMessage | str | None,
):
    """回复消息.

    Args:
        event (EventSchema): 消息事件.
        reply_message (List[Message] | Message | FileMessage | str | None): 回复内容.
    """
    if reply_message is None or not reply_message:
        return
    if event.is_room:
        is_room = "1"
        to = event.source.room.topic
    else:
        is_room = "0"
        to = event.source.from_user.name
    if isinstance(reply_message, FileMessage):
        files = {
            "content": (reply_message.filename, reply_message.content),
        }
        data = {
            "to": to,
            "isRoom": is_room,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(WX_BOT_API_V1, data=data, files=files)
    else:
        if isinstance(reply_message, str):
            reply_message = Message(type=MessageType.text, content=reply_message)
        reply = ReplyMessage(to=to, data=reply_message).model_dump(by_alias=True)
        async with httpx.AsyncClient() as client:
            response = await client.post(WX_BOT_API, json=reply)
    response.raise_for_status()
    assert response.json()["success"], response.text


async def run_command(router: CommandRouter, event: EventSchema):
    """路由命令执行.

    Args:
        router (CommandRouter): 命令路由器.
        event (EventSchema): 消息事件.
    """
    routes = router.matches(event)
    for route in routes:
        func = route.func
        if route.event_arg:
            func = partial(func, event)
        try:
            if asyncio.iscoroutinefunction(func):
                reply_message = await func(**route.func_kwargs)
            else:
                reply_message = func(**route.func_kwargs)
            await reply(event, reply_message)
        except Exception:
            import traceback

            log.error(traceback.format_exc())
            reply_message = await config.error_reply()
            await reply(event, reply_message)
