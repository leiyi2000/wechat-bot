import json
import httpx

from bot.command import CommandRouter


router = CommandRouter()


def convert_heat_to_number(heat_str):
    """将含有'万'的热度字符串转换为数字"""
    return float(heat_str.replace("万", "")) * 10000


@router.command("热搜", event_arg=False)
async def heat():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v.api.aa1.cn/api/bilibili-rs/")
        data = response.json()
        video_list = data["data"]
        video_list.sort(key=lambda x: convert_heat_to_number(x["heat"]), reverse=True)
        ranked_video_list = [
            {"rank": index + 1, **video} for index, video in enumerate(video_list)
        ][:15]
        return json.dumps(ranked_video_list, indent=4, ensure_ascii=False)
