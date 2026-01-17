from . import repository
from conflict import repository as cr


async def save_feedback(admin1, feedback, country, curr_user):
    res = cr.list_conflicts_by_admin1(admin1)

    if len(res) == 1:
        return repository.create_feedback(feedback, res[0].id, curr_user.id)

    res = cr.list_conflicts_by_admin1_and_country(admin1, country)

    if len(res) == 1:
        return repository.create_feedback(feedback, res[0].id, curr_user.id)

    return None
