"""牛马指令"""
from wechat.command import CommandRouter
from wechat.schemas import (
    Event,
    Message,
    MessageType,
    ReplyUserMessage,
    ReplyRoomMessage,
)


router = CommandRouter()


@router.command("牛马", event_arg=True)
async def setu(event: Event):
    message = Message(
        type=MessageType.file,
        content='https://api.anosu.top/img?$alias=cloud.jpg',
    )
    if event.is_room:
        reply = ReplyRoomMessage(
            to=event.source.room.payload.topic,
            data=message,
        )
    else:
        reply = ReplyUserMessage(
            to=event.source.from_user.name,
            data=message
        )
    return reply
