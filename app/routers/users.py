from fastapi import HTTPException, status, APIRouter
from .. import schemas, models, utils
from ..database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Posts"])


@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(dependency=get_db)):
    posts = db.query(models.User).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(body: schemas.CreateUser, db: Session = Depends(dependency=get_db)):
    # hash the password
    hased_pswrd = utils.hash(body.password)
    body.password = hased_pswrd

    new_user = models.User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(dependency=get_db)):
    user_details = db.query(models.User).filter(models.User.id == id).first()

    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this id"
        )

    return user_details
