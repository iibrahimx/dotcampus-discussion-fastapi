from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import admin, comments, discussions, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dot Campus Discussion API")

app.include_router(users.router)
app.include_router(discussions.router)
app.include_router(comments.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Dot Campus Discussion API is running"}
