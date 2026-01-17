from sqlmodel import Field, SQLModel


class ConflictBase(SQLModel):
    country: str = Field(index=True)


class Conflict(ConflictBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # country: str = Field(index=True)
    admin1: str = Field(index=True)
    population: int | None = Field(default=None, index=True)
    events: int = Field(default=None, index=True)
    score: int = Field(default=None, index=True)
