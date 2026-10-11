from fastapi import FastAPI
from database import Base, engine
from routers.v1 import users as users_v1
from routers.v2 import users as users_v2
from routers.v1 import accounts as accounts_v1

Base.metadata.create_all(bind=engine)

# TODO : Add OpenAPI documentation for the API using description
app = FastAPI(
    title="CampusBank API",
    description="""
CampusBank is a sample banking API for campus users.

## Features
- **Users v1 / v2** - create, list, fetch, update, and delete users
- **Accounts** - manage savings/current accounts under a user (max 5 per user)
- **Validation** - Pydantic schemas for request and response bodies
- **Persistence** - SQLite via SQLAlchemy with dependency-injected sessions

## Versions
- `/api/v1/users` - basic user fields
- `/api/v2/users` - includes user `id` and `account_count`
- `/api/v1/users/{username}/accounts` - account operations

Interactive docs: `/docs` (Swagger UI) and `/redoc`.
    """,
    version="2.0.0",
)

app.include_router(users_v1.router)
app.include_router(users_v2.router)
app.include_router(accounts_v1.router)

@app.get("/")
def root():
    return {"message": "Welcome to CampusBank API!"}