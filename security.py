import bcrypt, jwt, utils
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import dependencies, database, models, schemas
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

SECRET_KEY = "373b820b71449329c71f8168c46613a581afd84f3a3e82d32797dac9619697e0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, email: str):
    if utils.verify_email(email=email):
        return dependencies.get_user_by_email(db=db, email=email)
    raise HTTPException(status_code=422, detail="Invalid email format") 


def authenticate_user(db: Session, email: str, password: str):
    db_user = get_user(db=db, email=email)
    if not db_user:
        return False
    if not check_password(password, db_user.password):
        return False
    return db_user


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode(), salt)
    return hashed_password.decode()


def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    db_user = get_user(Session=Depends(database.get_db), email=token_data.email)
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user