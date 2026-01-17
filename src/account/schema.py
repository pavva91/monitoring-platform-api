from . import models


class Credentials(models.AccountBase):
    password: str


class AccountPublic(models.AccountBase):
    id: int
