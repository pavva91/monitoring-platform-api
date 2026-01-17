from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import FastAPI
from db import get_session
from fastapi_pagination import add_pagination
from fastapi_pagination import add_pagination
from starlette.middleware.gzip import GZipMiddleware
from fastapi import FastAPI
from api import api_router

app = FastAPI(
    title="Monitoring Platform API",
    description="The API must support user authentication, allow you to view information about conflicts in different countries, and allow the user to post feedback.",
    root_path="/api/v1",
    # docs_url=None,
    # openapi_url="/docs/openapi.json",
    # redoc_url="/docs",
)

SessionDep = Annotated[Session, Depends(get_session)]

add_pagination(app)

# we add all API routes to the Web API framework
app.include_router(api_router)

app.add_middleware(GZipMiddleware, minimum_size=1000)
