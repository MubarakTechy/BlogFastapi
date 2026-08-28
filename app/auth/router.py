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




# 4. Building a Strong Online Presence

# Title: Simple Ways to Build a Strong Online Presence

# Content:
# Building an online presence starts with having clear information about your business. A professional website, active social media profiles, useful content, and easy communication channels can help customers find and trust your business.

# 5. The Importance of Customer Experience

# Title: Why Customer Experience Matters

# Content:
# Customers remember how a business makes them feel. Providing quick responses, clear information, reliable services, and an easy purchasing process can improve customer satisfaction and encourage people to return.

# If you're testing your FastAPI blog endpoint, I can also give you 
# 10 posts in the exact JSON format for your /blogs POST request, including title, content, image_url, and any other fields your schema requires.