from typing import Callable, Any, List, Dict

import asyncio
from functools import partial

import httpx
import structlog

from wechat import config
from wechat.settings import WX_BOT_API
from wechat.schemas import (
    Message,
    MessageType,
    ReplyUserMessage,
    ReplyRoomMessage,
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
    event: EventSchema, reply_message: List[Message] | Message | str | None
):
    """回复消息.

    Args:
        event (EventSchema): 消息事件.
        reply_message (Message | str): 回复内容.
    """
    if reply_message is None or not reply_message:
        return
    if isinstance(reply_message, str):
        reply_message = Message(type=MessageType.text, content=reply_message)
    if event.is_room:
        reply = ReplyRoomMessage(
            to=event.source.room.topic,
            data=reply_message,
        )
    else:
        reply = ReplyUserMessage(
            to=event.source.from_user.name,
            data=reply_message,
        )
    async with httpx.AsyncClient() as client:
        await client.post(WX_BOT_API, json=reply.model_dump(by_alias=True))


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
        except Exception as e:
            log.error(e)
            reply_message = await config.error_reply()
        await reply(event, reply_message)
