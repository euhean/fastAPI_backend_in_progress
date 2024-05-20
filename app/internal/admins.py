from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies, schemas
from ..database import get_db

router = APIRouter(
    prefix="/admins",
    tags=["Admin"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)


@router.post("/signup/", response_model=schemas.Admin)
def signup(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = dependencies.get_admin_by_email(db=db, email=admin.email)
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dependencies.create_admin(db=db, admin=admin)


@router.put("/users/{user_id}/payment/")
def update_payment(user_id: int, db: Session = Depends(get_db)):
    db_user = dependencies.get_user(db=db, user_id=user_id)
    for meal in db_user.meals:
        if meal.paid == False:
            return {"message": f"Meal with id {meal.id} not paid yet"}
    db_user.paid = True
    db.commit()
    return {"message" : "User payment completed"}


@router.put("/meals/{meal_id}/payment")
def set_meal_paid(meal_id: int, db: Session = Depends(get_db)):
    db_meal = dependencies.get_meal(db=db, meal_id=meal_id)
    db_meal.paid = True
    db.commit()
    return {"message" : "Meal payment updated"}