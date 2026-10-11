from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User, UserInput, UserUpdate, UserResponseV2
from crud import create_user, get_all_users, get_user_by_username, update_user, delete_user

# TODO : Include the versioning in the router prefix and tags, e.g., prefix="/v2/users" and tags=["v2_users"]
router = APIRouter(
    ...
)

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@router.post("/", response_model=...)
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
@router.get("/{username}", response_model=...)
def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user:
        return {"id": user.id, "username": user.username, "email": user.email, "age": user.age, "account_count": len(user.accounts)}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to update the user's information using the username as a path parameter and Pydantic's UserUpdate model for validation
@router.put("/{username}", response_model=...)
def update_user_endpoint(username: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, username, user_update)
    if updated_user:
        return {"id": updated_user.id, "username": updated_user.username, "email": updated_user.email, "age": updated_user.age, "account_count": len(updated_user.accounts)}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a user using the username as a path parameter
@router.delete("/{username}", response_model=...)
def delete_user_endpoint(username: str, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, username)
    if deleted_user:
        return {"id": deleted_user.id, "username": deleted_user.username, "email": deleted_user.email, "age": deleted_user.age, "account_count": len(deleted_user.accounts)}
    else:
        raise HTTPException(status_code=404, detail="User not found")