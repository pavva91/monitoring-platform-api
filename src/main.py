from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination import add_pagination
from starlette.middleware.gzip import GZipMiddleware
from fastapi import FastAPI
from api import api_router

app = FastAPI(
    title="Monitoring Platform API",
    description="The API supports user authentication with RBAC authentication, allows you to view information about conflicts in different countries, and allow the user to post feedback and the admin to delete the records.",
    root_path="/api/v1",
)

add_pagination(app)

# NOTE: we add here all the API routes in the api_router
app.include_router(api_router)

app.add_middleware(GZipMiddleware, minimum_size=1000)
