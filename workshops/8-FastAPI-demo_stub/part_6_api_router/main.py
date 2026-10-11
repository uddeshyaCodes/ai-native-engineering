from fastapi import FastAPI
from database import Base, engine
from routers import users, accounts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusBank API",
    description= "Banking API for university students",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(accounts.router)

@app.get("/")
def root():
    return {"message": "Welcome to CampusBank API!"}