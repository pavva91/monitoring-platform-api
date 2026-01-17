from fastapi import APIRouter
from starlette.responses import JSONResponse
from pydantic import BaseModel

from account.router import account_router
from conflict.router import conflict_router
from feedback.router import feedback_router


class ErrorMessage(BaseModel):
    """Represents a single error message."""

    msg: str


class ErrorResponse(BaseModel):
    """Defines the structure for API error responses."""

    detail: list[ErrorMessage] | None = None


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


@api_router.get("/ping", include_in_schema=False)
def healthcheck():
    """Simple healthcheck endpoint."""
    return {"status": "pong"}


# NOTE: we add all API routes
api_router.include_router(account_router)
api_router.include_router(conflict_router)
api_router.include_router(feedback_router)
