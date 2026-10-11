from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from models import UserDB, AccountDB
from sqlalchemy.orm import Session
from schemas import User, UserInput

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Starting point of the API - Opening the base URL of the API
@app.get("/")
def root():
    return {"message": "Welcome to CampusBank API!"}

# Dependency Injection to get the database session for each request

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@app.post("/users")
def create_user(user: UserInput, db: Session = Depends(get_db)):
    # TODO: Implement the logic to create a new user in the database using the UserInput model for validation and serialization
    db_user = UserDB(username=user.username, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": db_user}

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the database
@app.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    # TODO: Implement the logic to retrieve all users from the database and return them as a list of User models
    users = db.query(UserDB).all()
    return users