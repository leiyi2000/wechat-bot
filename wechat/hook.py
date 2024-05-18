from typing import List

import httpx

from wechat.settings import WX_BOT_API, WX_BOT_API_V1
from wechat.schemas import (
    Message,
    FileMessage,
    MessageType,
    ReplyMessage,
)


async def reply(
    to: str,
    is_room: bool,
    reply_message: List[Message] | Message | FileMessage | str | None,
):
    """回复消息.

    Args:
        event (Event): 消息事件.
        reply_message (List[Message] | Message | FileMessage | str | None): 回复内容.
    """
    if reply_message is None or not reply_message:
        return
    if isinstance(reply_message, FileMessage):
        files = {
            "content": (reply_message.filename, reply_message.content),
        }
        data = {
            "to": to,
            "isRoom": "1" if is_room else "0",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(WX_BOT_API_V1, data=data, files=files)
    else:
        if isinstance(reply_message, str):
            reply_message = Message(type=MessageType.text, content=reply_message)
        reply = ReplyMessage(
            to=to,
            isRoom=is_room,
            data=reply_message,
        )
        reply = reply.model_dump(by_alias=True)
        async with httpx.AsyncClient() as client:
            response = await client.post(WX_BOT_API, json=reply)
    response.raise_for_status()
    assert response.json()["success"], response.text
