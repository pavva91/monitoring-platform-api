from fastapi import APIRouter

from account.router import account_router
from conflict.router import conflict_router
from feedback.router import feedback_router


api_router = APIRouter()


@api_router.get("/ping", include_in_schema=False)
def healthcheck():
    """Simple healthcheck endpoint."""
    return {"status": "pong"}


# NOTE: we add all API routes
api_router.include_router(account_router)
api_router.include_router(conflict_router)
api_router.include_router(feedback_router)
