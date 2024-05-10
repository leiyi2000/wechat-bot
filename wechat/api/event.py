"""消息事件"""
import json

import structlog
from fastapi import APIRouter, Form, BackgroundTasks

from wechat import task
from wechat.schemas import Event


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
    mentioned: int = Form(alias="isMentioned"),
    system_event: int = Form(alias="isSystemEvent"),
    msg_from_self: int = Form(alias="isMsgFromSelf"),
):
    event = {
        "type": type,
        "content": content,
        "source": json.loads(source),
        "mentioned": mentioned,
        "system_event": system_event,
        "msg_from_self": msg_from_self,
    }
    log.info(f"receive event: {event}")
    background_tasks.add_task(task.event_task, Event.model_validate(event))
