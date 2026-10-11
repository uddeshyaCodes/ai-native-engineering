from sqlalchemy import select
from sqlalchemy.orm import Session
from models import UserDB
from schemas import UserInput

# Function to create a new user in the database
def create_user(db: Session, user: UserInput):
    # TODO: Implement the logic to create a new user in the database using the UserInput model for validation and serialization
    db_user = UserDB(username=user.username, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to retrieve user by username from the database
def get_user_by_username(db: Session, username: str):
    # TODO: Implement the logic to retrieve a user by username from the database and return it as a User model
    user = db.scalar(select(UserDB).where(UserDB.username == username))
    return user

# Function to retrieve all users from the database
def get_all_users(db: Session):
    # TODO: Implement the logic to retrieve all users from the database and return them as a list of User models
    users = db.scalars(select(UserDB)).all()
    return users