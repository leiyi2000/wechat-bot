import json
import httpx

from bot.command import CommandRouter


router = CommandRouter()


@router.command("热搜", event_arg=False)
async def heat():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v.api.aa1.cn/api/bilibili-rs/")
        ranked_video = response.json()["data"].sort(
            key=lambda x: x["heat"], 
            reverse=True,
        )
        ranked_video = ranked_video[:10]
        return json.dumps(ranked_video, indent=4, ensure_ascii=False)
