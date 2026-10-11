from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, get_db
from models import UserDB, AccountDB
from sqlalchemy.orm import Session
from schemas import User, UserUpdate, UserInput
from crud import create_user, get_all_users, get_user_by_username, update_user, delete_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Starting point of the API - Opening the base URL of the API
@app.get("/")
def root():
    return {"message": "Welcome to CampusBank API!"}

# Dependency Injection to get the database session for each request

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@app.post("/users")
def create_user_endpoint(user: UserInput, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return {"message": "User created successfully", "user": db_user}

# Endpoint to retrieve all users from the database
@app.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

# Endpoint to access the user's account information using the username as a path parameter
@app.get("/users/{username}", response_model=User)
def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    # TODO: Implement the logic to retrieve a user by username from the database and return it as a User model
    user = get_user_by_username(db, username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to update the user's information using the username as a path parameter and Pydantic's UserUpdate model for validation
@app.put("/users/{username}", response_model=User)
def update_user_endpoint(username: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    # TODO: Implement the logic to update user details in the database using the UserUpdate model for validation and serialization
    user = update_user(db, username, user_update)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a user using the username as a path parameter
@app.delete("/users/{username}", response_model=User)
def delete_user_endpoint(username: str, db: Session = Depends(get_db)):
    # TODO: Implement the logic to delete a user from the database by username
    user = delete_user(db, username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")