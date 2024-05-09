from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies, schemas 
from ..database import get_db
from .users import read_user

router = APIRouter(
    prefix="/meals",
    tags=["Meal"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/users/{user_id}/meals/", response_model=schemas.Meal)
def create_meal_for_user(
        user_id: int, meal: schemas.MealCreate, db: Session = Depends(get_db)
    ):
    return dependencies.create_user_meal(db=db, meal=meal, user_id=user_id)


@router.get("/meals/", response_model=list[schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return dependencies.get_meals(db, skip=skip, limit=limit)


@router.get("/users/{user_id}/meals/", response_model=list[schemas.Meal])
def read_user_meals(user_id: int, db: Session = Depends(get_db)):
    return read_user(user_id=user_id, db=db).meals


@router.get("/users/meals/{meal_id}/", response_model=schemas.Meal)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = dependencies.get_meal(db=db, meal_id=meal_id)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return db_meal

@router.put("/users/meals/{meal_id}/", response_model=schemas.Meal)
def edit_meal(meal_id: int, meal: schemas.MealBase, db: Session = Depends(get_db)):
    db_meal = read_meal(meal_id=meal_id, db=db)
    for field, value in meal.dict().items():
        setattr(db_meal, field, value)
    db.commit()
    db.refresh(db_meal)
    return db_meal
