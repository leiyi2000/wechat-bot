"""服务入口"""
from fastapi import FastAPI

from wechat.api import router


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
