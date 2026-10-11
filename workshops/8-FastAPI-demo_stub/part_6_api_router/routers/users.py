from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User, UserUpdate, Account, UserInput
from crud import create_user, get_all_users, get_user_by_username, update_user, delete_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@router.post("/")
def create_user_route(user: UserInput, db: Session = Depends(get_db)):
    # TODO: Implement the logic to create a new user in the database using the UserInput model for validation and serialization
    user = create_user(user)
    return user
    raise HTTPException(status_code=400, detail="Invalid user input")

# Endpoint to get all users from the database and return them as a list of User objects
@router.get("/")
def get_users_route():
    # TODO: Implement the logic to retrieve all users from the database and return them as a list of User models
    ...

# Endpoint to access the user's account information using the username as a path parameter
@router.get("/{username}")
def get_user_by_username_endpoint():
    # TODO: Implement the logic to retrieve a user by username from the database and return it as a User model
    ...

# Endpoint to update the user's information using the username as a path parameter and Pydantic's UserUpdate model for validation
@router.put("/{username}")
def update_user_endpoint():
    # TODO: Implement the logic to update user details in the database using the UserUpdate model for validation and serialization
    ...

# Endpoint to delete a user using the username as a path parameter
@router.delete("/{username}")
def delete_user_endpoint():
    # TODO: Implement the logic to delete a user from the database by username
    ...