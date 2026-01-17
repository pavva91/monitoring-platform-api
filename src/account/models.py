from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


class AccountBase(SQLModel):
    username: str = Field(index=True)


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_type_id: int | None = Field(default=2, index=True)
    password_hash: str = Field(index=True)


class AccountPublic(AccountBase):
    id: int


class AccountCreate(AccountBase):
    password_hash: str = Field(index=True)


class AccountUpdate(AccountBase):
    password_hash: str = Field(index=True)
