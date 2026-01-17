from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from conflict import service
from db import get_session
from . import schemas
from sqlmodel import Session
from auth.authorization import get_current_user_authorization
from account import models as am


SessionDep = Annotated[Session, Depends(get_session)]

conflict_router = APIRouter()


@conflict_router.get("/conflictdata", response_model=list[schemas.ConflictResponse])
async def list_all(page: int = Query(default=1, ge=1), size: int = Query(default=20, le=100), countries: List[str] = Query(default=[])):
    return await service.list_conflicts(page, size, countries)


@conflict_router.get("/conflictdata/{country}", response_model=list[schemas.ConflictResponse])
async def get_country_details(country, session: SessionDep):
    return await service.get_country_details(country, session)


@conflict_router.get("/conflictdata/{country}/riskscore", response_model=schemas.AverageConflictScoreResponse)
async def get_average_risk_score(country: str):
    """
    select avg(score) from conflict where country=%s;
    """
    res = await service.get_average_risk_score(country)
    return res


@conflict_router.delete("/conflictdata", response_model=list[schemas.ConflictResponse])
async def bulk_delete_conflicts(
        admin1: str = Query(default=None),
        country: str = Query(default=None),
        _: am.Account = Depends(get_current_user_authorization)
):
    if admin1 is None and country is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insert at least one between admin1 or country",
        )

    return await service.delete_records(admin1, country)
