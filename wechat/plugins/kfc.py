
import httpx

from wechat.command import CommandRouter


router = CommandRouter()


@router.command("kfc", event_arg=False)
async def kfc():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.jixs.cc/api/wenan-fkxqs/index.php")
        return response.text
