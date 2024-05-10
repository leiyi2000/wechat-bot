from typing import List

from enum import StrEnum

from pydantic import BaseModel, Field


class EventRoomMember(BaseModel):

    avatar: str
    id: str
    name: str
    alias: str


class EventRoomPayload(BaseModel):

    adminIdList: List
    avatar: str
    id: str
    # 房间名称
    topic: str
    member_list: List[EventRoomMember] = Field(alias="memberList")


class EventRoom(BaseModel):

    _events: dict
    _eventsCount: int
    id: str
    payload: EventRoomPayload


class EventSourceFromPayload(BaseModel):

    alias: str
    avatar: str
    friend: bool
    gender: int
    id: str
    name: str
    phone: List
    province: str
    star: bool
    type: int


class EventSourceFrom(BaseModel):

    _events: dict
    _eventsCount: int
    id: str
    payload: EventSourceFromPayload


class EventSource(BaseModel):

    room: EventRoom
    to: dict
    from_user: EventSourceFrom = Field(alias="from")


class Event(BaseModel):

    type: str
    content: str
    source: EventSource
    mentioned: int
    system_event: int
    msg_from_self: int


class MessageType(StrEnum):
    """消息类型"""

    file = "fileUrl"
    text = "text"


class Message(BaseModel):
    """消息"""

    type: MessageType
    content: str


class ReplyRoomMessage(BaseModel):
    """回复消息"""
    
    to: str
    is_room: bool = Field(default=True, alias="isRoom")
    data: List[Message] | Message
