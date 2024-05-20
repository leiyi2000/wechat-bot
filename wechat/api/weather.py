from fastapi import APIRouter

from wechat import models


router = APIRouter()


@router.get(
    "",
    description="查询天气任务列表",
)
async def reads():
    return await models.Weather.all()
