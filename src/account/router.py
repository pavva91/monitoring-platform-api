from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
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


class HTTPErrorUserAlreadyExist(BaseModel):
    detail: str = "user with this username already exists"
    pass


@account_router.post(
    "/register",
    response_model=schema.AccountResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPErrorUserAlreadyExist,
            "description": "user with this username already exists",
        }
    },
)
async def create_new_reader_user(
    creds: schema.AccountCredentialsRequest, session: SessionDep
):
    res = await service.create_user(session, creds)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this username already exists",
        )

    else:
        return res


class HTTPErrorWrongCreds(BaseModel):
    detail: str = "Wrong username and password"
    pass


@account_router.post(
    "/login",
    response_model=None,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPErrorWrongCreds,
            "description": "Wrong username and password",
        }
    },
)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    jwt = await service.authenticate_user(form_data.username, form_data.password)
    return jwt


class HTTPErrorNoJWT(BaseModel):
    detail: str = "Not authenticated"
    pass


@account_router.post(
    "/logout",
    response_model=None,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPErrorNoJWT,
            "description": "Not authenticated",
        }
    },
)
async def logout_user(
    curr_user: am.Account = Depends(get_current_user_authorization),
) -> schemas.Token:
    res = await service.register_logout(curr_user)
    return res
