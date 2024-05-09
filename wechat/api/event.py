"""消息事件"""
import structlog
from fastapi import APIRouter, Form


router = APIRouter()
log = structlog.get_logger()


@router.post(
    "",
    description="消息上报",
)
async def receive(
    type: str = Form(...),
    content: str = Form(...),
    source: str = Form(...),
    mentioned: int = Form(alias="isMentioned"),
    system_event: int = Form(alias="isSystemEvent"),
    msg_from_self: int = Form(alias="isMsgFromSelf"),
):
    event = {
        "type": type,
        "content": content,
        "source": source,
        "mentioned": mentioned,
        "system_event": system_event,
        "msg_from_self": msg_from_self,
    }
    log.info(f"receive event: {event}")
