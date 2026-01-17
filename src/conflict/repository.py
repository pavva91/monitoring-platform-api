from typing import List
from . import models
from db import DatabaseSession
from sqlmodel import select, func, and_


def get_country_details(db_session, country: str):
    stmt = select(
        models.Conflict
    ).where(
        func.lower(models.Conflict.country) == func.lower(country))
    return db_session.exec(stmt)


def list_conflicts(skip: int, size: int):
    stmt = select(
        models.Conflict
    ).order_by(
        models.Conflict.id
    ).offset(skip).limit(size)
    with DatabaseSession() as db:
        return db.exec(stmt).all()


def list_conflicts_in_countries(skip: int, size: int, countries: List[str]):
    stmt = select(
        models.Conflict
    ).where(
        func.lower(models.Conflict.country).in_(countries)
    ).order_by(models.Conflict.id).offset(skip).limit(size)

    with DatabaseSession() as db:
        return db.exec(stmt).all()


def list_conflicts_by_admin1(admin1: str):
    with DatabaseSession() as db:
        stmt = select(
            models.Conflict
        ).where(
            func.lower(models.Conflict.admin1) == func.lower(admin1))
        return db.exec(stmt).all()


def list_conflicts_by_admin1_and_country(admin1: str, country: str):
    with DatabaseSession() as db:
        stmt = select(
            models.Conflict
        ).where(
            and_(
                func.lower(models.Conflict.admin1) == func.lower(admin1),
                func.lower(models.Conflict.country) == func.lower(country)
            ))
        return db.exec(stmt).all()
