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


@router.post("/users/{user_id}/", response_model=schemas.Meal)
def create_meal_for_user(
        user_id: int, meal: schemas.MealCreate, db: Session = Depends(get_db)
    ):
    return dependencies.create_user_meal(db=db, meal=meal, user_id=user_id)


@router.get("/", response_model=list[schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return dependencies.get_meals(db=db, skip=skip, limit=limit)


@router.get("/users/{user_id}/", response_model=list[schemas.Meal])
def read_user_meals(user_id: int, db: Session = Depends(get_db)):
    return read_user(user_id=user_id, db=db).meals


@router.get("/{meal_id}/", response_model=schemas.Meal)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = dependencies.get_meal(db=db, meal_id=meal_id)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return db_meal

@router.put("/{meal_id}/edit_meal/", response_model=schemas.Meal)
def edit_meal(meal_id: int, meal: schemas.MealBase, db: Session = Depends(get_db)):
    db_meal = read_meal(meal_id=meal_id, db=db)
    for field, value in meal.model_dump().items():
        setattr(db_meal, field, value)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.delete("/{meal_id}/delete_meal/")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = read_meal(meal_id=meal_id, db=db)
    db.delete(db_meal)
    db.commit()
    return {"message": "Meal deleted succesfully"}