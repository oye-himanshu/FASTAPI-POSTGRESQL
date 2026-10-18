from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import Oauth2, schemas, database, models
from .. import utils

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: schemas.UserLogin,
    db: Session = Depends(dependency=database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    #  checking weather the password enter by user is correct or not
    is_password_matched = utils.verify(user_credentials.password, user.password)
    if not is_password_matched:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # now we generate a jwt token
    access_token = Oauth2.create_access_token(
        data={
            "id": user.id,
        }
    )

    return {"access_token": access_token, "token_type": "Bearer"}
