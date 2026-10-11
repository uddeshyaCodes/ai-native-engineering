from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User, UserInput, UserUpdate, UserResponseV2
from crud import create_user, get_all_users, get_user_by_username, update_user, delete_user

router = APIRouter(
    prefix="/api/v2/users",
    tags=["Users - V2"]
)

# TODO :  Add the description for the router and endpoints using OpenAPI documentation features, including summary, description, and responses for this endpoint
# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@router.post(
    "/",
    response_model=UserResponseV2,
    status_code=201,
    summary="Create a new User",
    description="""
Register a new CampusBank user (API v2).

Returns an enriched payload with database `id` and current `account_count` (starts at 0).
Fails with **400** if the username is already taken.
    """,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Username already registered"},
        422: {"description": "Validation error in request body"},
    },
)
def create_user_route(user: UserInput, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = create_user(db, user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email, "age": db_user.age, "account_count": len(db_user.accounts)}

# Endpoint to get all users from the database and return them as a list of User objects
@router.get("/", response_model=list[User])
def get_users_route(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

# Endpoint to access the user's account information using the username as a path parameter
@router.get("/{username}", response_model=UserResponseV2)
def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user:
        return {"id": user.id, "username": user.username, "email": user.email, "age": user.age, "account_count": len(user.accounts)}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# TODO : Add the description for the router and endpoints using OpenAPI documentation features, including summary, description, and responses for this endpoint
# Endpoint to update the user's information using the username as a path parameter and Pydantic's UserUpdate model for validation
@router.put(
    "/{username}",
    response_model=UserResponseV2,
    summary="Update a User Details",
    description="""
Partially update a user's email and/or age by username (API v2).

Only fields present in the body are applied. Returns the v2 user shape including `id` and `account_count`.
Fails with **404** if the user does not exist.
    """,
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        422: {"description": "Validation error in request body"},
    },
)
def update_user_endpoint(username: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, username, user_update)
    if updated_user:
        return {"id": updated_user.id, "username": updated_user.username, "email": updated_user.email, "age": updated_user.age, "account_count": len(updated_user.accounts)}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a user using the username as a path parameter
@router.delete("/{username}", response_model=UserResponseV2)
def delete_user_endpoint(username: str, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, username)
    if deleted_user:
        return {"id": deleted_user.id, "username": deleted_user.username, "email": deleted_user.email, "age": deleted_user.age, "account_count": len(deleted_user.accounts)}
    else:
        raise HTTPException(status_code=404, detail="User not found")