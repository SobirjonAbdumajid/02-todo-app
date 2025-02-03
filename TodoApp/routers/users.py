from fastapi import APIRouter, Depends, HTTPException, status
from ..database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from ..models import Users
from passlib.context import CryptContext
from pydantic import BaseModel


class UserVerification(BaseModel):
    password: str
    new_password: str


router = APIRouter(
    prefix="/user",
    tags=["users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/")
async def get_user(user: user_dependency, db: db_dependency):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()

    return current_user


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Authorization Failed")

    if not bcrypt_context.verify(user_verification.password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    current_user.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(current_user)
    db.commit()


@router.put('/phonenumber/{new_phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone(user: user_dependency, db: db_dependency, new_phone_number):
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Authorization Failed - put")
    current_user.phone_number = new_phone_number
    db.add(current_user)
    db.commit()
