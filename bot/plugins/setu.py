from typing import List

import httpx
import structlog

from bot import alist
from bot.config import config
from bot.command import CommandRouter
from bot.schemas import (
    Message,
    MessageType,
)


router = CommandRouter()
history_setu: List[str] = []
log = structlog.get_logger()


@router.command("st", event_arg=False)
async def setu():
    async with httpx.AsyncClient() as client:
        response = await client.get(config.setu.api, follow_redirects=True)
        url = str(response.url)
    if history_setu:
        history_setu[-1] = url
    else:
        history_setu.append(url)
    return Message(type=MessageType.file, content=url)


@router.command("sts", event_arg=False)
async def sts():
    if history_setu and config.alist.enable:
        url = history_setu[-1]
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        filename = f'setu/{url.split("/")[-1]}'
        file_url = await alist.upload(
            api=config.alist.api,
            api_key=config.alist.api_key,
            path=config.alist.path,
            filename=filename,
            content=response.content,
        )
        return file_url
    else:
        raise ValueError("sts not get history_setu or alist disable")
