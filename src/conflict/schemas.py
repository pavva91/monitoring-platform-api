from decimal import Decimal
from pydantic import BaseModel, field_validator
from . import models


class AverageConflictScoreResponse(BaseModel):
    average: Decimal

    @field_validator("average")
    @classmethod
    def round_average(cls, v: Decimal) -> Decimal:
        return round(v, 2)


class ConflictResponse(models.ConflictBase):
    id: int
    country: str
    admin1: str
    population: int | None
    events: int
    score: int
