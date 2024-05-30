from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import dependencies, schemas
from typing import Annotated
from ..database import get_db
from ...security import* 


router = APIRouter(
    prefix="/admins",
    tags=["Admin"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)


@router.post("/token/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    admin = authenticate_user(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup/", response_model=schemas.Admin)
def signup(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = dependencies.get_admin_by_email(db=db, email=admin.email)
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dependencies.create_admin(db=db, admin=admin)


@router.put("/{user_id}/payment/")
def update_payment(user_id: int, db: Session = Depends(get_db)):
    db_user = dependencies.get_user(db=db, user_id=user_id)
    for meal in db_user.meals:
        if meal.paid == False:
            return {"message": f"Meal with id {meal.id} not paid yet"}
    db_user.paid = True
    db.commit()
    return {"message" : "User payment completed"}


@router.put("/{meal_id}/payment")
def set_meal_paid(meal_id: int, db: Session = Depends(get_db)):
    db_meal = dependencies.get_meal(db=db, meal_id=meal_id)
    db_meal.paid = True
    db.commit()
    return {"message" : "Meal payment updated"}