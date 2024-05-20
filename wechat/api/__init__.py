"""路由配置"""

from fastapi import APIRouter

from wechat.api import event, config, weather


router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


router.include_router(
    event.router,
    prefix="/event",
    tags=["事件上报"],
)


router.include_router(
    config.router,
    prefix="/config",
    tags=["配置"],
)


router.include_router(
    weather.router,
    prefix="/weather",
    tags=["天气"],
)