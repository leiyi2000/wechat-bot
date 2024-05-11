"""牛马指令"""
from wechat.command import CommandRouter
from wechat.schemas import (
    Message,
    MessageType,
)


router = CommandRouter()
anosu = 'https://api.anosu.top/img?$alias=cloud.jpg'


@router.command("牛马", event_arg=False)
async def setu():
    return Message(type=MessageType.file, content=anosu)
