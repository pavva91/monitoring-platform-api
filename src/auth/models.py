from sqlmodel import Field, SQLModel
from datetime import datetime


class Logout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: int | None = Field(index=True)
    last_logout_on: datetime = Field(index=True)
