from . import models
from fastapi import Query
from pydantic import BaseModel

class FeedbackInput(BaseModel):
    text: str = Query(min_length=10, max_length=500)

class FeedbackResponse(models.FeedbackBase):
    id: int
    conflict_id: int
