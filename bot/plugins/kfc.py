import httpx

from bot.config import config
from bot.command import CommandRouter


router = CommandRouter()


@router.command("kfc", event_arg=False)
async def kfc():
    api = await config.kfc_api()
    async with httpx.AsyncClient() as client:
        response = await client.get(api)
        response.raise_for_status()
    return response.text