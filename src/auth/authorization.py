from datetime import datetime, timezone
import casbin
from fastapi import HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer

from . import authentication
from . import schemas
from account import repository
from account import models
from jwt.exceptions import InvalidTokenError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        jwt = authentication.decode_jwt(token)
        if jwt is None:
            raise credentials_exception
        username = jwt.get("sub")
        role = jwt.get("role")
        issued_at_timestamp = jwt.get("iat")
        if username is None or role is None or issued_at_timestamp is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=role)

        user = repository.get_account_by_username(
            username_in=token_data.username)
        if user is None:
            raise credentials_exception

        logouts = repository.get_logout_by_account_id(user.id)
        if len(logouts) == 1:
            last_logout_on_timestamp = logouts[0].last_logout_on.timestamp()
            # NOTE: always normalize to utc
            issued_at = datetime.fromtimestamp(
                issued_at_timestamp, timezone.utc)
            last_logout_on = datetime.fromtimestamp(
                last_logout_on_timestamp, timezone.utc)
            if last_logout_on > issued_at:
                raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    return user


# NOTE: casbin authorization middleware
async def get_current_user_authorization(req: Request, curr_user: models.Account = Depends(get_current_user)):
    e = casbin.Enforcer("casbin/model.conf", "casbin/policy.csv")
    user_role = ''
    match curr_user.account_type_id:
        case 1:
            user_role = 'admin'
        case 2:
            user_role = 'reader'
        case _:
            raise credentials_exception

    sub = user_role
    obj = req.url.path
    act = req.method
    if not (e.enforce(sub, obj, act)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Method not authorized for this user")
    return curr_user
