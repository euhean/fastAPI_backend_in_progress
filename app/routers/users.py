from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies, schemas
from ..database import get_db
from ... import utils

router = APIRouter(
    prefix="/users",
    tags=["User"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.post("/signup/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = dependencies.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dependencies.create_user(db=db, user=user)


@router.put("/{user_id}/edit_profile/", response_model=schemas.User)
def edit_user_profile(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    data = user.model_dump().items()
    db_user = read_user(user_id=user_id, db=db)
    for field, value in data:
        if field == 'email':
            if not utils.verify_email(value):
                raise HTTPException(status_code=422, detail="Invalid email format")
        if field == 'birthdate':
            if not utils.verify_birthdate(value):
                raise HTTPException(status_code=422, detail="You must be 18 years or older")
        if field == 'password':
            if not utils.verify_password(value):
                raise HTTPException(status_code=422, detail="Invalid password format")
        if field == 'telephone':
            if not utils.verify_telephone(value):
                raise HTTPException(status_code=422, detail="Invalid phone number")
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}/delete_profile/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = read_user(user_id=user_id, db=db)
    db.delete(db_user)
    db.commit()
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