from bot.config import config
from bot.command import CommandRouter
from bot.schemas import (
    Message,
    MessageType,
)


router = CommandRouter()


@router.command("st", event_arg=False)
async def setu():
    return Message(type=MessageType.file, content=config.setu.api)
