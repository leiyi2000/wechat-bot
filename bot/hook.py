from typing import List

import httpx

from bot import alist
from bot.config import config
from bot.settings import WX_BOT_API, WX_BOT_API_V1
from bot.schemas import (
    Message,
    FileMessage,
    MessageType,
    ReplyMessage,
)


async def file_by_alist(
    reply_message: FileMessage,
) -> Message:
    """发送文件.

    Args:
        reply_message (FileMessage): 文件消息.

    Returns:
        Message: 回复消息.
    """
    file_url = await alist.upload(
        api=config.alist.api,
        api_key=config.alist.api_key,
        path=config.alist.path,
        filename=reply_message.filename,
        content=reply_message.content,
    )
    return Message(type=MessageType.file, content=file_url)


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
    # 消息转换
    if isinstance(reply_message, str):
        reply_message = Message(type=MessageType.text, content=reply_message)
    elif isinstance(reply_message, FileMessage) and config.alist.enable:
        reply_message = await file_by_alist(reply_message)
    # 本地文件上传
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
