import json
import httpx
from wechat import config
from wechat.schemas import Event
from wechat.command import CommandRouter
from typing import List, Dict, Any

router = CommandRouter()


@router.command("新闻")
async def get_news(event: Event):
    type = event.content.removeprefix("新闻").strip()
    news_api_key = await config.news_api_key()
    params = {"key": news_api_key, "type": type, "page_size": 10, "is_filter": 1}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://v.juhe.cn/toutiao/index", params=params, headers=headers
        )
        data = response.json()["result"]["data"]
        result_data: List[Dict[str, Any]] = [
            {
                "title": item["title"],
                "date": item["date"],
                "author_name": item["author_name"],
                "url": item["url"],
            }
            for item in data
        ]
    return json.dumps(result_data, indent=4, ensure_ascii=False)
