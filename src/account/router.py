from typing import Annotated

from fastapi import Depends, Query
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm


from fastapi import APIRouter

from auth.authorization import get_current_user_authorization
from . import service
from . import schema
from db import get_session
from auth import schemas
from account import models as am

account_router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@account_router.post("/register", response_model=schema.AccountPublic)
async def register(creds: schema.Credentials, session: SessionDep):
    return await service.create_user(session, creds)


@account_router.post("/login", response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    return await service.authenticate_user(form_data.username, form_data.password)


@account_router.get("/users", response_model=list[schema.AccountPublic])
async def list_all_users(
    page: int = Query(default=1, ge=1),
    size: Annotated[int, Query(le=100)] = 10,
    _: am.Account = Depends(get_current_user_authorization)
):
    return service.list_users(page, size)
