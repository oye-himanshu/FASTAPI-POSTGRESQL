#  in this file you are gonna to learn how to use SQLalcahmy (ORM).

from fastapi import FastAPI, HTTPException, status
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Server started successfully."}


@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(dependency=get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(dependency=get_db)):
    # new_post = models.Post(title=post.title, content= post.content,publish=post.publish)
    # instead of writing above code we use the below code (what if there are 50 fields)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(dependency=get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with this id"
        )
    return posts


@app.delete("/posts/{id}", response_model=schemas.Post)
def delete_post_by_id(id: int, db: Session = Depends(dependency=get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()

    if posts == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with this id"
        )
    db.delete(posts)
    db.commit()
    return posts


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, body: schemas.UpdatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with this id"
        )

    post_query.update(
        {
            models.Post.title: body.title,
            models.Post.content: body.content,
            models.Post.publish: body.publish,
        },
        synchronize_session=False,
    )

    db.commit()
    db.refresh(post)

    return post
