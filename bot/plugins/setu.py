from bot.config import config
from bot.command import CommandRouter
from bot.schemas import (
    Message,
    MessageType,
)


router = CommandRouter()


@router.command("st", event_arg=False)
async def setu():
    api = await config.setu_api()
    return Message(type=MessageType.file, content=api)
