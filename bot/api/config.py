from fastapi import APIRouter, Body

from bot.models import Config
from bot.config import config as bot_config


router = APIRouter()


@router.post(
    "",
    description="添加或者修改一项配置",
)
async def create_or_update(
    key: str = Body(),
    value: str = Body(),
):
    config = await Config.get_or_none(key=key)
    if config is None:
        config = await Config.create(key=key, value=value)
    else:
        config.value = value
        await config.save()
    # 同步更新
    bot_config.load(key, value)
    return config
