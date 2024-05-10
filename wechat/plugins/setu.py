"""牛马指令"""
from wechat.command import CommandRouter
from wechat.schemas import (
    Event,
    Message,
    MessageType,
    ReplyRoomMessage,
)


router = CommandRouter()


@router.command("牛马", event_arg=True)
async def setu(event: Event):
    print(event)
    return ReplyRoomMessage(
        to=event.source.room.payload.topic,
        data=Message(
            type=MessageType.file,
            content='https://api.anosu.top/img?$alias=cloud.jpg',
        )
    )
