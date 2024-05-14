import os

import httpx
import jinja2

from wechat import render
from wechat.config import config
from wechat.command import CommandRouter
from wechat.settings import TEMPLATE_DIR
from wechat.schemas import Event, FileMessage


router = CommandRouter()


@router.command("查天气")
async def real_time_weather(event: Event):
    address = event.content.removeprefix("查天气").strip()
    api_key = await config.weather_api_key()
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": api_key,
        "address": address,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        city_code = response.json()["geocodes"][0]["adcode"]
    params = {
        "key": api_key,
        "city": city_code,
        "extensions": "base",
        "output": "JSON",
    }
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
    # 读取模板内容
    with open(
        os.path.join(TEMPLATE_DIR, "weather.html.jinja2"), encoding="utf-8"
    ) as file:
        template = jinja2.Template(file.read())
    assert len(response.json()["lives"]) > 0
    html = template.render(weather=response.json())
    image = await render.html_to_image(html, dom="#main")
    return FileMessage(filename="weather.png", content=image)
