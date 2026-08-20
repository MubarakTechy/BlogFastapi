from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.service import (
    get_user_by_email,
    get_user_by_username,
    get_admin_by_email,
    create_user,
    verify_password,
    create_access_token,
    create_admin_access_token
)
from app.auth.schemas import UserCreate, UserResponse, LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_email = get_user_by_email(
        db,
        user_data.email
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered try another email"
        )

    existing_username = get_user_by_username(
        db,
        user_data.username
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken try another name"
        )

    return create_user(
        db,
        user_data.username,
        user_data.email,
        user_data.password
    )


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(
        db,
        login_data.email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password you can also register if you don't have an account"
        )

    password_valid = verify_password(
        login_data.password,
        user.password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password please check your credentials and try again"
        )

    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/admin-login")
def admin_login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    admin = get_admin_by_email(
        db,
        login_data.email
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please you are not an admin  you can only login if you are an admin"
        )

    password_valid = verify_password(
        login_data.password,
        admin.hashed_password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin email or password please check your credentials and try again"
        )

    access_token = create_admin_access_token(admin)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }