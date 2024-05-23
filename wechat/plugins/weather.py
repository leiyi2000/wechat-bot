import os
from functools import partial
from datetime import datetime, timedelta

import httpx
import jinja2
import structlog

from wechat import hook
from wechat.config import config
from wechat import render, models
from wechat.command import CommandRouter
from wechat.schedule import Job, schedule
from wechat.schemas import Event, FileMessage
from wechat.settings import TEMPLATE_DIR, SHANGHAI_TIMEZONE


router = CommandRouter()
log = structlog.get_logger()


class WeatherType:
    """天气类型"""

    rain = "rain"


async def get_adcode(api_key: str, address: str) -> str:
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": api_key,
        "address": address,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()["geocodes"][0]["adcode"]


@router.command("天气")
async def real_time_weather(event: Event):
    address = event.content.removeprefix("天气").strip()
    api_key = await config.weather_api_key()
    adcode = await get_adcode(api_key, address)
    params = {
        "key": api_key,
        "city": adcode,
        "extensions": "base",
        "output": "JSON",
    }
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
    # 读取模板内容
    with open(
        os.path.join(TEMPLATE_DIR, "weather.html.jinja2"),
        encoding="utf-8",
    ) as file:
        template = jinja2.Template(file.read())
    assert len(response.json()["lives"]) > 0
    html = template.render(weather=response.json())
    image = await render.html_to_image(html, dom="#main")
    return FileMessage(filename="weather.png", content=image)


@router.command("下雨提醒")
async def rain_remind(event: Event):
    args = event.content.removeprefix("下雨提醒").strip().split("#")
    if len(args) == 1:
        address = args[0]
        at_hour = "20"
    else:
        address, at_hour = args
    try:
        at_hour = int(at_hour)
        assert 0 < at_hour < 23, "Invalid range"
        api_key = await config.weather_api_key()
        adcode = await get_adcode(api_key, address)
        weather = await models.Weather.get_or_none(
            to=event.to,
            is_room=event.is_room,
            adcode=adcode,
        )
        if weather is None:
            await models.Weather.create(
                to=event.to,
                is_room=event.is_room,
                at_hour=at_hour,
                adcode=adcode,
                address=address,
                type=WeatherType.rain,
            )
        else:
            weather.at_hour = at_hour
            await weather.save()
        message = f"作为你的机器女友, {address}如果下雨我将在{at_hour}点提醒你"
    except Exception:
        message = "添加失败"
    print(f"message: {message}")
    return message


@router.command("取消下雨提醒")
async def cancel_rain_remind(event: Event):
    address = event.content.removeprefix("取消下雨提醒").strip()
    if not address:
        await models.Weather.filter(to=event.to, is_room=event.is_room).delete()
        message = "删库跑路了~~"
    else:
        api_key = await config.weather_api_key()
        adcode = await get_adcode(api_key, address)
        weather = await models.Weather.get_or_none(
            to=event.to, is_room=event.is_room, adcode=adcode
        )
        if weather:
            await weather.delete()
        message = "哼~哼~, 再也不关心你了"
    return message


@schedule.job(at="* * 18 * *", tz=SHANGHAI_TIMEZONE)
async def rain_remind_job():
    now = datetime.now(tz=SHANGHAI_TIMEZONE)
    async for weather in models.Weather.filter(type=WeatherType.rain):
        api_key = await config.weather_api_key()
        params = {
            "key": api_key,
            "city": weather.adcode,
            "extensions": "all",
            "output": "JSON",
        }
        url = "https://restapi.amap.com/v3/weather/weatherInfo"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
        forecasts = response.json()["forecasts"]
        tomorrow_weather = forecasts[0]["casts"][1]
        if "雨" in (desc := tomorrow_weather["dayweather"]):
            # 准备发送消息
            reply_message = f"亲~, {weather.address}有{desc}"
            func = partial(hook.reply, weather.to, weather.is_room, reply_message)
            send_datetime = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=weather.at_hour,
                tzinfo=SHANGHAI_TIMEZONE,
            )
            send_datetime += timedelta(days=1)
            job = Job(func, once=send_datetime)
            schedule.add_job(job)
