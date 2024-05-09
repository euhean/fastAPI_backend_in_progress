from sqlalchemy.orm import Session
from . import models, schemas
from typing import Annotated
from fastapi import Header, HTTPException


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


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_password = user.password + "fakedpass"
    db_user = models.User(**user.dict(), password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_meal(db: Session, meal_id: int):
    return db.query(models.Meal).filter(models.Meal.id == meal_id).first()


def get_meals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meal).offset(skip).limit(limit).all()


def create_user_meal(db: Session, meal: schemas.MealCreate, user_id: int):
    db_meal = models.Meal(**meal.dict(), user_id=user_id)
    db.add(db_meal)
    db.commit
    db.refresh(db_meal)
    return db_meal