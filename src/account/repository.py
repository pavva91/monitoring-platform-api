from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session, select, update

from . import models
from auth import models as auth_models
from db import get_session
from db import DatabaseSession


SessionDep = Annotated[Session, Depends(get_session)]


def create_account(session: Session, account: models.AccountCreate) -> models.Account:
    db_account = models.Account.model_validate(account)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


def get_account(session: Session, id: int) -> models.Account:
    account = session.get(models.Account, id)
    if not account:
        raise HTTPException(status_code=404, detail="Hero not found")
    return account


def get_account_by_username(username_in: str):
    with DatabaseSession() as db:
        account = db.exec(
            select(models.Account).filter_by(username=username_in)
        ).first()
    return account


def get_logout_by_account_id(account_id: str):
    stmt = select(auth_models.Logout).where(auth_models.Logout.account_id == account_id)
    with DatabaseSession() as db:
        logout = db.exec(stmt).all()
        return logout


def update_logout_date(account_id: int):
    stmt = (
        update(auth_models.Logout)
        .where(auth_models.Logout.account_id == account_id)
        .values(last_logout_on=datetime.now(timezone.utc))
    )

    with DatabaseSession() as db:
        db.exec(stmt)
        db.commit()
        return


def create_logout(account_id: int):
    logout_dict = {
        "account_id": account_id,
        "last_logout_on": datetime.now(timezone.utc),
    }
    with DatabaseSession() as db:
        db_logout = auth_models.Logout.model_validate(logout_dict)
        db.add(db_logout)
        db.commit()
        db.refresh(db_logout)
        return db_logout
