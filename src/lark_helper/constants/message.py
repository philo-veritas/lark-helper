from enum import StrEnum


class MessageType(StrEnum):
    """
    接受消息内容结构
    https://open.feishu.cn/document/server-docs/im-v1/message-content-description/message_content
    """

    TEXT = "text"
    POST = "post"
    IMAGE = "image"
    FILE = "file"
    AUDIO = "audio"
    VIDEO = "video"
    STICKER = "sticker"
    INTERACTIVE = "interactive"


class ReceiveIdType(StrEnum):
    CHAT_ID = "chat_id"
    OPEN_ID = "open_id"
    USER_ID = "user_id"
