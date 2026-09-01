from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


# ==========================================
# CREATE COURSE REGISTRATION
# ==========================================

class CourseRegistrationCreate(BaseModel):
    full_name: str
    email: EmailStr
    course: str
    city: str
    state: str
    other: str | None = None
    reason: str


# ==========================================
# RESPONSE
# ==========================================

class CourseRegistrationResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    full_name: str
    email: EmailStr
    course: str
    city: str
    state: str
    other: str | None
    reason: str
    created_at: datetime