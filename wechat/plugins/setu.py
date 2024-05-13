"""ST指令"""

from wechat import config
from wechat.command import CommandRouter
from wechat.schemas import (
    Message,
    MessageType,
)


router = CommandRouter()


@router.command("st", event_arg=False)
async def setu():
    api = await config.setu_api()
    return Message(type=MessageType.file, content=api)
