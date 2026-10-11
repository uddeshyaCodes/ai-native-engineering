from fastapi import FastAPI
from database import Base, engine
from routers.v1 import users as users_v1
from routers.v2 import users as users_v2
from routers.v1 import accounts as accounts_v1

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusBank API",
    description= "Banking API for university students",
    version="1.0.0"
)

app.include_router(users_v1.router)
app.include_router(users_v2.router)
app.include_router(accounts_v1.router)

@app.get("/")
def root():
    return {"message": "Welcome to CampusBank API!"}