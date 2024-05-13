from fastapi import APIRouter

from wechat.models import Config
from wechat.config import ConfigKey


router = APIRouter()


@router.post(
    "",
    description="添加或者修改一项配置",
)
async def create_or_update(
    key: ConfigKey,
    value: str,
):
    config = await Config.get_or_none(key=key)
    if config is None:
        config = await Config.create(key=key, value=value)
    else:
        config.value = value
        await config.save()
    return config
