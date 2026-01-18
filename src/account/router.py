from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm


from fastapi import APIRouter

from . import service
from . import schema
from db import get_session
from auth import schemas
from account import models as am
from auth.authorization import get_current_user_authorization

account_router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@account_router.post("/register", response_model=schema.AccountResponse)
async def register(creds: schema.AccountCredentialsRequest, session: SessionDep):
    return await service.create_user(session, creds)


@account_router.post("/login", response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    jwt = await service.authenticate_user(form_data.username, form_data.password)
    return jwt


@account_router.post("/logout", response_model=None)
async def logout(
    curr_user: am.Account = Depends(get_current_user_authorization)
) -> schemas.Token:
    res = await service.register_logout(curr_user)
    return res
