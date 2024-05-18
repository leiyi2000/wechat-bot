import httpx

from wechat import render
from wechat.schemas import FileMessage
from wechat.command import CommandRouter


router = CommandRouter()


@router.command("每日一题", event_arg=False)
async def day():
    # 判断是否过期
    url = "https://leetcode.cn/graphql"
    payload = {
        "query": "query CalendarTaskSchedule($days: Int!) {calendarTaskSchedule(days: $days) {contests {  id  name  slug  progress  link  premiumOnly}dailyQuestions {  id  name  slug  progress  link  premiumOnly}studyPlans {  id  name  slug  progress  link  premiumOnly}}}",
        "variables": {"days": 0},
        "operationName": "CalendarTaskSchedule",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
    link = response.json()["data"]["calendarTaskSchedule"]["dailyQuestions"][0]["link"]
    # 请求地址渲染图片
    image = await render.url_to_image(link, dom=".flexlayout__tab")
    file_message = FileMessage(filename="leetcode.png", content=image)
    return file_message
