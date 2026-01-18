from datetime import datetime, timezone, timedelta
from sqlmodel import Session
from fastapi import HTTPException

from auth.authentication import create_jwt_token

from . import utils
from . import schema
from . import models
from . import repository


async def create_user(session: Session, creds: schema.AccountCredentialsRequest):
    account = repository.get_account_by_username(creds.username)
    if account is not None:
        return None

    acc = models.AccountCreate(
        username=creds.username, password_hash=utils.hash_password(creds.password))
    db_account = repository.create_account(session, acc)
    return db_account


async def authenticate_user(username: str, password: str):
    account = repository.get_account_by_username(username)
    if not account:
        raise HTTPException(
            status_code=401, detail="Wrong username and password")

    if not utils.verify_password(account.password_hash, password):
        raise HTTPException(
            status_code=401, detail="Wrong username and password")

    account_type = ''
    match account.account_type_id:
        case 1:
            account_type = 'admin'
        case 2:
            account_type = 'reader'
        case _:
            raise Exception('invalid account type id')

    jwt = create_jwt_token(account.username, account_type)
    return jwt


async def register_logout(account):
    # TODO: check if already exists record
    logouts = repository.get_logout_by_account_id(account.id)
    if len(logouts) > 1:
        raise Exception('this should not happen')

    is_present = True if len(logouts) == 1 else False

    if is_present:
        res = repository.update_logout_date(account.id)
    else:
        res = repository.create_logout(account.id)
    return res
