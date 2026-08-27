from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer

from app.database import Base


# ==========================================
# USER
# ==========================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


# ==========================================
# BLOG
# ==========================================

class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    admin_id: Mapped[int] = mapped_column(
        ForeignKey("admins.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    admin: Mapped["Admin"] = relationship(
        "Admin",
        back_populates="blogs"
    )


# ==========================================
# JOB
# ==========================================

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    company: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    requirements: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    salary: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    job_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    image_url: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True
)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    author: Mapped["User"] = relationship()


# ==========================================
# CONTACT
# ==========================================

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ==========================================
# ADMIN
# ==========================================

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    blogs: Mapped[list["Blog"]] = relationship(
        "Blog",
        back_populates="admin"
    )









    

    

#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         index=True
#     )

#     full_name: Mapped[str] = mapped_column(
#         String(100),
#         nullable=False
#     )

#     email: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False,
#         index=True
#     )

#     message: Mapped[str] = mapped_column(
#         Text,
#         nullable=False
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=datetime.utcnow,
#         nullable=False
#     )


# # ==========================================
# # ADMIN
# # ==========================================

# class Admin(Base):
#     __tablename__ = "admins"

#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         index=True
#     )

#     email: Mapped[str] = mapped_column(
#         String,
#         unique=True,
#         index=True,
#         nullable=False
#     )

#     hashed_password: Mapped[str] = mapped_column(
#         String,
#         nullable=False
#     )

#     blogs: Mapped[list["Blog"]] = relationship(
#         "Blog",
#         back_populates="admin"
#     )