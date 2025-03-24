from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import dependencies, schemas, models
from ..database import get_db
from ... import utils
from typing import Annotated
from ...security import *


router = APIRouter(
    prefix="/users",
    tags=["User"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.post("/token/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #Send email to new users
    return dependencies.create_user(db=db, user=user)


@router.put("/edit_profile/", response_model=schemas.User)
def edit_user_profile(user: schemas.UserBase, db: Session = Depends(get_db)):
    data = user.model_dump().items()
    db_user = Depends(get_current_active_user)
    for field, value in data:
        if field == 'email':
            if not utils.verify_email(value):
                raise HTTPException(status_code=422, detail="Invalid email format")
            #Send email to new adress
        if field == 'telephone':
            if not utils.verify_telephone(value):
                raise HTTPException(status_code=422, detail="Invalid phone number")
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/delete_profile/")
def delete_user(db: Session = Depends(get_db)):
    db_user = Depends(get_current_active_user)
    db.delete(db_user)
    db.commit()
    return {"message": "User  deleted succesfully"}


@router.get("/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/me/meals/", response_model=list[schemas.Meal])
async def read_own_meals(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user.meals


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return dependencies.get_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = dependencies.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user