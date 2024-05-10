import json


a = """{"type": "text", "content": "what", "source": {"room": {}, "to": {"_events": {}, "_eventsCount": 0, "id": "@24b3fc1cd2cbdaebe3754946195c7145bdb70904af035412e3549e58d0a41189", "payload": {"alias": "", "avatar": "http://localhost:3001/resouces?media=%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxgeticon%3Fseq%3D1020139554%26username%3D%4024b3fc1cd2cbdaebe3754946195c7145bdb70904af035412e3549e58d0a41189%26skey%3D%40crypt_50080d85_f82ef74c48cd54f17f6e90a12a512a4d", "friend": false, "id": "@24b3fc1cd2cbdaebe3754946195c7145bdb70904af035412e3549e58d0a41189", "name": "yuwu", "phone": [], "star": false, "type": 1}}, "from": {"_events": {}, "_eventsCount": 0, "id": "@e44b0fc5be810acf3e384777cdb8dbaa23a37cb86fc4b4bc28ef2c4b37521514", "payload": {"address": "", "alias": "雨勿", "avatar": "http://localhost:3001/resouces?media=%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxgeticon%3Fseq%3D853550155%26username%3D%40e44b0fc5be810acf3e384777cdb8dbaa23a37cb86fc4b4bc28ef2c4b37521514%26skey%3D", "city": "", "friend": true, "gender": 1, "id": "@e44b0fc5be810acf3e384777cdb8dbaa23a37cb86fc4b4bc28ef2c4b37521514", "name": "雨勿", "phone": [], "province": "", "signature": " 米有", "star": false, "weixin": "", "type": 1}}}, "mentioned": 0, "system_event": 0, "msg_from_self": 0}"""


event = json.loads(a)

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
    gender: int
    name: str
    phone: List
    province: str
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

    @property
    def is_room(self):
        return self.room is not None


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


class ReplyUserMessage(BaseModel):
        
    to: str
    data: List[Message] | Message


EventSource(**event["source"])
Event(**event)