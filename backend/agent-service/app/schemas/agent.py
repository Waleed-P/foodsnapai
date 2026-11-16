from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, description="User's question or message for the nutrition agent.")


class ChatResponse(BaseModel):
    response: str
    user_id: int
