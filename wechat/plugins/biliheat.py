import json

import httpx

from wechat.command import CommandRouter


router = CommandRouter()


def convert_heat_to_number(heat_str):
    """将含有'万'的热度字符串转换为数字"""
    return float(heat_str.replace("万", "")) * 10000


@router.command("热搜", event_arg=False)
async def biliheat():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v.api.aa1.cn/api/bilibili-rs/")
        data = response.json()
        if data["msg"] == "获取成功":
            video_list = data["data"]
            video_list.sort(
                key=lambda x: convert_heat_to_number(x["heat"]), reverse=True
            )
            ranked_video_list = [
                {"rank": index + 1, **video} for index, video in enumerate(video_list)
            ]
            # 将结果序列化为JSON格式的字符串
            return json.dumps(ranked_video_list, ensure_ascii=False, indent=4)
        else:
            return json.dumps({"error": "获取失败"}, ensure_ascii=False)
