from enum import StrEnum

from pydantic import BaseModel, Field


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: Role = Field(
        ...,
        description="The role of the message sender",
        examples=[Role.SYSTEM, Role.USER, Role.ASSISTANT],
    )
    content: str = Field(
        ...,
        description="Text content from system, user, or assistant"
    )

