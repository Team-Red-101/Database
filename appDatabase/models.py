import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Prompt(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    prompt: str = Field(...)
    question: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "prompt": "Doesn't seem like you should be doing that bud.",
                "question": "Okie dokie did you throw away your trash buddy?"
            }
        }

class PromptUpdate(BaseModel):
    prompt: Optional[str]
    question: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Doesn't seem like you should be doing that bud.",
                "question": "Okie dokie did you throw away your trash buddy?"
            }
        }