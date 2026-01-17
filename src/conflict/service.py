from decimal import Decimal
from . import repository


async def list_conflicts(page: int, size: int, countries):
    skip = (page - 1) * size
    if len(countries) == 0:
        return repository.list_conflicts(skip=skip, size=size)

    return repository.list_conflicts_in_countries(skip=skip, size=size, countries=countries)


async def get_country_details(country, session):
    return repository.get_country_details(session, country)


async def get_average_risk_score(country):
    res = await repository.get_avg_by_country(country)
    return res[0]


async def delete_records(admin1, country):
    if country is not None and admin1 is not None:
        repository.delete_conflicts_by_admin1_and_country(
            admin1, country)
        return

    if country is None:
        repository.delete_conflicts_by_admin1(admin1)
        return

    if admin1 is None:
        repository.delete_conflicts_by_country(country)
        return
