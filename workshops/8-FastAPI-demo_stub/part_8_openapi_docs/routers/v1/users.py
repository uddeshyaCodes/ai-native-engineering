from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User, UserInput, UserUpdate, UserResponseV1
from crud import create_user, get_all_users, get_user_by_username, update_user, delete_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users - V1"]
)

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@router.post("/", response_model=User)
def create_user_route(user: UserInput, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = create_user(db, user)
    return db_user

# Endpoint to get all users from the database and return them as a list of User objects
@router.get("/", response_model=list[User])
def get_users_route(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

# Endpoint to access the user's account information using the username as a path parameter
@router.get("/{username}", response_model=UserResponseV1)
def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user:
        return {"username": user.username, "email": user.email, "age": user.age}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to update the user's information using the username as a path parameter and Pydantic's UserUpdate model for validation
@router.put("/{username}", response_model=User)
def update_user_endpoint(username: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, username, user_update)
    if updated_user:
        return updated_user
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a user using the username as a path parameter
@router.delete("/{username}", response_model=User)
def delete_user_endpoint(username: str, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, username)
    if deleted_user:
        return deleted_user
    else:
        raise HTTPException(status_code=404, detail="User not found")