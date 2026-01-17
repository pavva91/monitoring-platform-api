from . import models


class AccountCredentialsRequest(models.AccountBase):
    password: str


class AccountResponse(models.AccountBase):
    id: int
