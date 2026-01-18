import jwt
from datetime import datetime, timezone


from config import settings

from . import schemas

JWT_ISSUER = "example.org"


def create_jwt_token(username: str, account_type: str) -> schemas.Token:
    now = datetime.now(timezone.utc)
    now_ts = now.timestamp()

    # NOTE: expire in 10' for testing purposes
    # expiration = now + 10 * 60

    # NOTE: reallistic value
    expiration = now_ts + 60 * 60 * 24
    payload = {
        "iss": JWT_ISSUER,  # NOTE: https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.1
        "sub": username,  # NOTE:https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.2
        "role": account_type,
        "iat": now_ts,  # NOTE: https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.6
        "exp": expiration,  # NOTE: https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.4
    }
    access_token = jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return schemas.Token(access_token=access_token, token_type="bearer")


def decode_jwt(token: str) -> dict | None:
    now = datetime.now(timezone.utc).timestamp()
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[
                                   settings.JWT_ALGORITHM])
        expires_at_timestamp = decoded_token.get("exp")
        if expires_at_timestamp is None:
            return None
        return decoded_token if decoded_token["exp"] >= now else None
    except Exception:
        return None
