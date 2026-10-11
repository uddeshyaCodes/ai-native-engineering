from sqlalchemy import select
from sqlalchemy.orm import Session
from models import AccountDB, UserDB
from schemas import User, UserUpdate, Account

# USER CRUD OPERATIONS

# Function to create a new user in the database
def create_user(db: Session, user: User):
    db_user = UserDB(username=user.username, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to retrieve user by username from the database
def get_user_by_username(db: Session, username: str):
    return db.scalar(select(UserDB).where(UserDB.username == username))

# Function to retrieve all users from the database
def get_all_users(db: Session):
    return db.scalars(select(UserDB)).all()

# Function to update user details in the database
def update_user(db: Session, username: str, user_update: UserUpdate):
    # TODO: Implement the logic to update user details in the database using the UserUpdate model for validation and serialization
    user = get_user_by_username(db, username)
    if user:
        user.username = user_update.username
        user.email = user_update.email
        user.age = user_update.age
        db.commit()
        db.refresh(user)
        return user
    return None

# Function to delete a user from the database
def delete_user(db: Session, username: str):
    # TODO: Implement the logic to delete a user from the database by username
    user = get_user_by_username(db, username)
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}