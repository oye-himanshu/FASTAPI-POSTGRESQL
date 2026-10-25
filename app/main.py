#  in this file you are gonna to learn how to use SQLalchamy (ORM).


from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def home():
    return {"message": "Server started successfully."}
