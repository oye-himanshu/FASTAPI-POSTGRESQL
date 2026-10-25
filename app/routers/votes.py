from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from .. import schemas, Oauth2

from app.schemas import VoteCreate

router = APIRouter(prefix="/vote", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def action_on_vote(
    body: VoteCreate,
    current_user: schemas.User = Depends(Oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    post = db.query(models.Post).filter(models.Post.id == body.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist."
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.posts_id == body.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    print(found_vote, "found_votefound_votefound_votefound_vote")

    if body.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This post is already voted",
            )
        new_vote = models.Vote(user_id=current_user.id, posts_id=body.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This vote does not found",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}


@router.get("/")
def get_votes(
    current_user: schemas.User = Depends(Oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    vote_query = db.query(models.Vote).all()
    return {"data": vote_query}
