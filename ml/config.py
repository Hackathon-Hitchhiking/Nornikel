from pydantic import BaseModel, Field


class ModelKwargs(BaseModel):
    temperature: float | None = Field(default=0.7)
    top_k: int | None = Field(default=30)
    top_p: float | None = Field(default=0.9)
    max_tokens: int | None = Field(default=8192, ge=1, le=8192)
    repeat_penalty: float = Field(default=1.1)
