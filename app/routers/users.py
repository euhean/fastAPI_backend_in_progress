from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies, schemas 
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = dependencies.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dependencies.create_user(db=db, user=user)


@router.put("/{user_id}/", response_model=schemas.User)
def edit_user_profile(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = read_user(user_id=user_id, db=db)
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = read_user(user_id=user_id, db=db)
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User  deleted succesfully"}


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return dependencies.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = dependencies.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

