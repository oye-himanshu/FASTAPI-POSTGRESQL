from fastapi import HTTPException, status, APIRouter

from app.Oauth2 import get_current_user
from .. import schemas, models
from ..database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from .. import Oauth2

router = APIRouter(prefix="/posts", tags=["Users"])


@router.get("/", response_model=list[schemas.Post])
def get_posts(
    db: Session = Depends(dependency=get_db),
    get_current_user: schemas.User = Depends(Oauth2.get_current_user),
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.created_by == get_current_user.id)
        .all()
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# get_current_user=Depends(Oauth.get_current_user) is passed to verify is user login or not
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(dependency=get_db),
    get_current_user: schemas.User = Depends(Oauth2.get_current_user),
):
    # new_post = models.Post(title=post.title, content= post.content,publish=post.publish)
    # instead of writing above code we use the below code (what if there are 50 fields)
    new_post = models.Post(created_by=get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post_by_id(
    id: int,
    db: Session = Depends(dependency=get_db),
    get_current_user: schemas.User = Depends(Oauth2.get_current_user),
):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with this id"
        )

    if posts.created_by != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this post.",
        )

    return posts


@router.delete("/{id}", response_model=schemas.Post)
def delete_post_by_id(
    id: int,
    db: Session = Depends(dependency=get_db),
    get_current_user: schemas.User = Depends(Oauth2.get_current_user),
):
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    posts = posts_query.first()

    if posts == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with this id"
        )
    if posts.created_by != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this post.",
        )

    db.delete(posts)
    db.commit()
    return posts


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    body: schemas.UpdatePost,
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(Oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with this id"
        )

    if post.created_by != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this post.",
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
