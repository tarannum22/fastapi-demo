from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, schemas, oauth2
from ..database import Session, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("total_likes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("total_likes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No post with id of {id}")
    return post

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = post_query.first()
    if current_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No post with id of {id}")
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not Authorised to perform requested action")    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No post with id of {id}")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not Authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
