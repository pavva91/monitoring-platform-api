from sqlmodel import Field, SQLModel

class FeedbackBase(SQLModel):
    text: str = Field(index=True)


class Feedback(FeedbackBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: int = Field(default=None, index=True)
    conflict_id: int = Field(default=None, index=True)
