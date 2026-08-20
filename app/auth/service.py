import bcrypt

from jose import jwt
from sqlalchemy.orm import Session

from app.models import User, Admin
from app.database import settings
from datetime import datetime, timedelta, timezone


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def get_user_by_email(
    db: Session,
    email: str
):
    return db.query(User).filter(
        User.email == email
    ).first()


def get_user_by_username(
    db: Session,
    username: str
):
    return db.query(User).filter(
        User.username == username
    ).first()


def get_admin_by_email(
    db: Session,
    email: str
):
    return db.query(Admin).filter(
        Admin.email == email
    ).first()


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
):
    hashed_password = hash_password(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_access_token(user: User):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_admin": user.is_admin,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def create_admin_access_token(admin: Admin):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(admin.id),
        "email": admin.email,
        "is_admin": True,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token