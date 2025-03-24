from sqlalchemy.orm import Session
import models, schemas
from typing import Annotated
from fastapi import Header, HTTPException
from .. import utils, security


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    user.password = security.hash_password(user.password)
    data = user.model_dump()
    db_user = models.User(**data)
    for field, value in data.items():
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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_admin(db: Session, admin: schemas.AdminCreate):
    admin.password = security.hash_password(admin.password)
    data = admin.model_dump()
    db_admin = models.Admin(**data)
    for field, value in data.items():
        if field == 'email':
            if not utils.verify_email(value):
                raise HTTPException(status_code=422, detail="Invalid email format")
        elif field == 'birthdate':
            if not utils.verify_birthdate(value):
                raise HTTPException(status_code=422, detail="You must be 18 years or older")
        elif field == 'password':
            if not utils.verify_password(value):
                raise HTTPException(status_code=422, detail="Invalid password format")
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_meal(db: Session, meal_id: int):
    return db.query(models.Meal).filter(models.Meal.id == meal_id).first()


def get_meals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meal).offset(skip).limit(limit).all()


def create_user_meal(db: Session, meal: schemas.MealCreate, user_id: int):
    db_meal = models.Meal(**meal.model_dump(), user_id=user_id)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal