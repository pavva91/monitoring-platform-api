from sqlmodel import Field, SQLModel


class AccountBase(SQLModel):
    username: str = Field(index=True)


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_type_id: int | None = Field(default=2, index=True)
    password_hash: str = Field(index=True)


class AccountCreate(AccountBase):
    password_hash: str = Field(index=True)
