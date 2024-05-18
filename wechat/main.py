"""服务入口"""

import asyncio

from contextlib import asynccontextmanager

from aerich import Command
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from wechat.api import router
from wechat.plugins import schedule
from wechat.settings import APP_NAME, TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    command = Command(
        tortoise_config=TORTOISE_ORM,
        app=APP_NAME,
        location="./migrations",
    )
    await command.init()
    await command.upgrade(run_in_transaction=True)
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=False,
    )
    # 执行注入的job
    asyncio.create_task(schedule.run())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
