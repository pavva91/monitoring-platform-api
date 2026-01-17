import jwt
import time

from config import settings

from . import schemas


def create_jwt_token(username: str, account_type: str) -> schemas.Token:
    payload = {
        "role": account_type,
        "expires": time.time() + 600,
        "sub": username,
        "iat": time.time()
    }
    access_token = jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return schemas.Token(access_token=access_token, token_type="bearer")


def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[
                                   settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None
