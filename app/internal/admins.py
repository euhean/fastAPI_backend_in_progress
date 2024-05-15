from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import dependencies, models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


@router.put("/users/{user_id}/payment/")
def update_payment(user_id: int, db: Session = Depends(get_db)):
    db_user = dependencies.get_user(db=db, user_id=user_id)
    for meal in db_user.meals:
        if meal.paid == False:
            return {"message": f"Meal with id {meal.id} not paid yet"}
    db_user.paid = True
    db.commit()
    return {"message" : "User payment complete"}


