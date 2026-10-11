from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from models import UserDB, AccountDB
from sqlalchemy.orm import Session
from schemas import User, UserInput
from crud import create_user, get_all_users

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
    # TODO: Implement the logic to create a new user in the database using the UserInput model for validation and serialization
    return create_user(user, db)

# Endpoint to retrieve all users from the database
@app.get("/users", response_model=list[User])
def get_users_endpoint(db: Session = Depends(get_db)):
    # TODO: Implement the logic to retrieve all users from the database and return them as a list of User models
    return get_all_users(db)