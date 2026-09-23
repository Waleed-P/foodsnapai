from fastapi import APIRouter, HTTPException, Depends
from app.model.user import UserModel
from app.schema.user import UserCreateSchema
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import (hash_password)

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register")
def register(
    user: UserCreateSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed = hash_password(
        user.password
    )

    new_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    } 