from typing import List

import os
import json

import httpx

from wechat import config
from wechat.command import CommandRouter
from wechat.schemas import (
    Event,
    Message,
    MessageType,
)


router = CommandRouter()
# 加载高德地图城市编码
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), './data/weather_amap_city.json'), 'r') as file:
    #  [["圣方济各堂区", "820008"]]
    city_code: List[List[str]] = json.load(file)


def get_city_code(city: str) -> str | None:
    for name, code in city_code:
        if city == name or name.startswith(city):
            return code


async def amap_weather(city: str) -> Message:
    if (city_code := get_city_code(city)) is None:
        content = '啊哦, 没有找到该城市'
    else:
        params = {
            "key": await config.weather_api_key(),
            "city": city_code,
            "extensions": "base",
            "output": "JSON",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get('https://restapi.amap.com/v3/weather/weatherInfo', params=params)
        if response.is_success:
            content = json.dumps(response.json(), indent=4, ensure_ascii=False)
        else:
            content = f'{city} 天气查询失败'
    return Message(type=MessageType.text, content=content)


@router.command("查天气")
async def real_time_weather(event: Event):
    return await amap_weather(event.content.removeprefix("查天气").strip())
