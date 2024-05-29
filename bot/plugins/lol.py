import os
import json

import httpx
import jinja2

from bot import render
from bot.config import config
from bot.command import CommandRouter
from bot.settings import TEMPLATE_DIR
from bot.schemas import Event, FileMessage


router = CommandRouter()


async def get_headers() -> dict:
    cookie = await config.lol_wegame_cookie()
    return {
        "Referer": "https://www.wegame.com.cn/helper/lol/v2/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/91.0.4472.164"
        "Safari/537.36 qblink wegame.exe"
        " WeGame/5.6.6.12275 ChannelId/0"
        "QBCore/91.1.23+g04c8d56+chromium-91.0.4472.164"
        "QQBrowser/9.0.2524.400",
        "HOST": "www.wegame.com.cn",
        "Cookie": cookie,
    }


@router.command("lol搜索")
async def player_search(event: Event):
    headers = await get_headers()
    nickname = event.content.removeprefix("lol搜索").strip()
    url = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer"
    async with httpx.AsyncClient() as client:
        payload = {
            "nickname": nickname,
            "from_src": "lol_helper",
        }
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
    # 添加nickname
    data = response.json()
    for player in data["players"]:
        player["name"] = nickname
    data = json.dumps(data, indent=4, ensure_ascii=False)
    with open(
        os.path.join(TEMPLATE_DIR, "lol_search.html.jinja2"),
        encoding="utf-8",
    ) as file:
        template = jinja2.Template(file.read())
        html = template.render(data=data)
        image = await render.html_to_image(html, dom="#main")
    return FileMessage(filename="weather.png", content=image)


@router.command("lol战绩")
async def battle(event: Event):
    headers = await get_headers()
    id, area = event.content.removeprefix("lol战绩").split("#")
    async with httpx.AsyncClient() as client:
        url = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleList"
        payload = {
            "account_type": 2,
            "area": area.strip(),
            "id": id.strip(),
            "count": 8,
            "filter": "",
            "offset": 0,
            "from_src": "lol_helper",
        }
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
    return json.dumps(response.json(), indent=4, ensure_ascii=False)


@router.command("lol对局")
async def battle_detail(event: Event):
    headers = await get_headers()
    id, area, game_id = event.content.removeprefix("lol对局").split("#")
    async with httpx.AsyncClient() as client:
        url = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleDetail"
        payload = {
            "account_type": 2,
            "area": area.strip(),
            "id": id.strip(),
            "game_id": game_id.strip(),
            "from_src": "lol_helper",
        }
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
    return json.dumps(response.json(), indent=4, ensure_ascii=False)
