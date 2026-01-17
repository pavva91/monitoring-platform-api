from . import repository


async def list_conflicts(page: int, size: int, countries):
    skip = (page - 1) * size
    if len(countries) == 0:
        return repository.list_conflicts(skip=skip, size=size)

    return repository.list_conflicts_in_countries(skip=skip, size=size, countries=countries)


async def get_country_details(country, session):
    return repository.get_country_details(session, country)
