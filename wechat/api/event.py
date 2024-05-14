"""消息事件"""
import json

import structlog
from fastapi import APIRouter, Form, BackgroundTasks

from wechat.schemas import Event
from wechat.command import run_command
from wechat.plugins import router as plugin_router


router = APIRouter()
log = structlog.get_logger()


@router.post(
    "",
    description="消息上报",
)
async def receive(
    background_tasks: BackgroundTasks,
    type: str = Form(...),
    content: str | bytes = Form(...),
    source: str = Form(...),
    mentioned: int = Form(alias="isMentioned", default=0),
    system_event: int = Form(alias="isSystemEvent", default=0),
    msg_from_self: int = Form(alias="isMsgFromSelf", default=0),
):
    event = {
        "type": type,
        "content": content,
        "source": json.loads(source),
        "mentioned": mentioned,
        "system_event": system_event,
        "msg_from_self": msg_from_self,
    }
    log.info(f"receive event: {json.dumps(event, ensure_ascii=False)}")
    background_tasks.add_task(run_command, plugin_router, Event.model_validate(event))
