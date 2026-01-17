from . import models


class ConflictResponse(models.ConflictBase):
    id: int
    country: str
    admin1: str
    population: int | None
    events: int
    score: int

    class Config:
        from_attributes = True
