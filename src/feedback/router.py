from fastapi import APIRouter, HTTPException, Query, Depends, status
from pydantic import BaseModel

from . import schemas
from . import service
from account import models as am
from auth.authorization import get_current_user_authorization


feedback_router = APIRouter()


class HTTPErrorNotAuthorized(BaseModel):
    detail: str = 'Method not authorized for this user'
    pass


@feedback_router.post("/conflictdata/{admin1}/userfeedback", response_model=schemas.FeedbackResponse, responses={
    status.HTTP_401_UNAUTHORIZED: {"model": HTTPErrorNotAuthorized,
                                   "description": "Correctly logged in user but not authorized role (e.g. admin)"}
})
async def reader_user_send_feedback(
    admin1: str,
    feedback: schemas.FeedbackInput,
    country: str = Query(default=None),
    curr_user: am.Account = Depends(get_current_user_authorization)
):
    res = await service.save_feedback(admin1, feedback, country, curr_user)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the admin1 related record",
        )

    return res
