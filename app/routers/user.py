from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, schemas, utils
from ..database import Session, get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash Logic
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except models.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User already exists with {user.email}. Use another email.")
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No User with id of {id}")
    return user
