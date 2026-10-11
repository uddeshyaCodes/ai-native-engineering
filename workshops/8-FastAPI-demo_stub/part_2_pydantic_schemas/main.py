from fastapi import FastAPI
from schemas import User, UserInput

app = FastAPI()

# In-memory storage for users
users = []

# Starting point of the API - Opening the base URL of the API
@app.get("/")
def root():
    return {"message": "Welcome to CampusBank API!"}

# Endpoint to create a new user using Pydantic's User model for validation and serialization, and store it in the in-memory list
@app.post("/users")
def create_user(user: UserInput):
    # TODO: Implement logic to create a new user and add it to the in-memory list
    users.append(user)
    return {"message": "User created successfully", "user": user.model_dump()}

# Endpoint to retrieve all users stored in the in-memory list
@app.get("/users", response_model=list[User])
def get_users():
    # TODO: Implement logic to retrieve and return all users from the in-memory list
    return users