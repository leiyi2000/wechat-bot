from typing import List

from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class EventRoomMember(BaseModel):

    avatar: str
    id: str
    name: str
    alias: str


class EventRoom(BaseModel):

    id: str
    adminIdList: List
    avatar: str
    # 房间名称
    topic: str
    member_list: List[EventRoomMember] = Field(alias="memberList")


class EventUser(BaseModel):

    id: str
    alias: str
    avatar: str
    friend: bool
    name: str
    phone: List
    star: bool
    type: int


class EventSource(BaseModel):

    room: EventRoom | None
    to: EventUser | None
    from_user: EventUser | None = Field(alias="from")

    @field_validator("room", mode="before")
    def validate_room(value):
        if "payload" in value:
            return EventRoom(**value["payload"])
        else:
            return None

    @field_validator("to", mode="before")
    def validate_to(value):
        if "payload" in value:
            return EventUser(**value["payload"])
        else:
            return None

    @field_validator("from_user", mode="before")
    def validate_from_user(value):
        if "payload" in value:
            return EventUser(**value["payload"])
        else:
            return None


class Event(BaseModel):

    type: str
    content: str
    source: EventSource
    mentioned: int
    system_event: int
    msg_from_self: int

    @property
    def is_room(self):
        return self.source.room is not None


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


class ReplyUserMessage(BaseModel):
        
    to: str
    data: List[Message] | Message
