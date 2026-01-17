from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from . import models
from db import get_session
from db import DatabaseSession


SessionDep = Annotated[Session, Depends(get_session)]


def create_account(session: Session, account: models.AccountCreate) -> models.Account:
    db_hero = models.Account.model_validate(account)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def get_account(session: Session, id: int) -> models.Account:
    account = session.get(models.Account, id)
    if not account:
        raise HTTPException(status_code=404, detail="Hero not found")
    return account


def get_account_by_username(username_in: str):
    with DatabaseSession() as db:
        account = db.exec(select(models.Account).filter_by(
            username=username_in)).first()
    # account = session.exec(select(models.Account).filter_by(username=username_in)).first()
    return account
