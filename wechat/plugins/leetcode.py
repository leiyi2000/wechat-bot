import httpx

from wechat import render
from wechat.schemas import FileMessage
from wechat.command import CommandRouter


router = CommandRouter()


@router.command("每日一题", event_arg=False)
async def day():
    url = "https://leetcode.cn/graphql/"
    payload = {
        "query": "\n    query CalendarTaskSchedule($days: Int!) {\n  calendarTaskSchedule(days: $days) {\n    contests {\n      id\n      name\n      slug\n      progress\n      link\n      premiumOnly\n    }\n    dailyQuestions {\n      id\n      name\n      slug\n      progress\n      link\n      premiumOnly\n    }\n    studyPlans {\n      id\n      name\n      slug\n      progress\n      link\n      premiumOnly\n    }\n  }\n}\n    ",
        "variables": {
            "days": 0
        },
        "operationName": "CalendarTaskSchedule"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
    link = response.json()["data"]["calendarTaskSchedule"]["dailyQuestions"][0]["link"]
    # 调用link渲染图片
    image = await render.url_to_image(link, dom=".flexlayout__tab")
    return FileMessage(filename="leetcode.png", content=image)
