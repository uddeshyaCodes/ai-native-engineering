from fastapi import FastAPI

app = FastAPI()

# In-memory storage for users
users = []

# Starting point of the API - Opening the base URL of the API
@app.get("/")
def root():
    # TODO: Return a welcome message or basic information about the API
    return {"message": "Welcome to CampusBank API!"}

# Endpoint to create a new user and store it in the in-memory list
@app.post("/users")
def create_user(user: dict):
    # TODO: Implement logic to create a new user and add it to the in-memory list
    users.append(user)
    return {"message": "User created successfully", "user": user}

# Endpoint to retrieve all users stored in the in-memory list
@app.get("/users")
def get_users():
    # TODO: Implement logic to retrieve and return all users from the in-memory list
    return {"users": users}