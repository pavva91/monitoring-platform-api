from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from conflict import service
from db import get_session
from . import schemas
from sqlmodel import Session


SessionDep = Annotated[Session, Depends(get_session)]

conflict_router = APIRouter()


@conflict_router.get("/conflictdata", response_model=list[schemas.ConflictResponse])
async def list_all(page: int = Query(default=1, ge=1), size: int = Query(default=20, le=100), countries: List[str] = Query(default=[])):
    return await service.list_conflicts(page, size, countries)


@conflict_router.get("/conflictdata/{country}", response_model=list[schemas.ConflictResponse])
async def get_country_details(country, session: SessionDep):
    return await service.get_country_details(country, session)


# # NOTE: 'anonymous' user can do
# @conflict_router.get("/conflictdata/{country}/riskscore", response_model=None)
# async def get_average_risk_score(country: str, q: str | None = None, short: bool = False):
#     item = {"item_id": country }
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

# # NOTE: also 'normal' user can do (ACL)
# @conflict_router.post("/conflictdata/{admin1}/userfeedback", response_model=None)
# async def save_user_feedback(admin1: str, item: Conflict):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         # item_dict['price_with_tax'] = price_with_tax
#         item_dict.update({'price_with_tax': price_with_tax})
#     return item_dict


# # NOTE: only admin can do (ACL)
# @conflict_router.delete("/conflictdata", response_model=None)
# async def delete_user_feedback(item: Conflict):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         # item_dict['price_with_tax'] = price_with_tax
#         item_dict.update({'price_with_tax': price_with_tax})
#     return item_dict
