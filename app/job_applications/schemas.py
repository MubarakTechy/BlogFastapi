from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr
)


# ==========================================
# CREATE APPLICATION
# ==========================================

class JobApplicationCreate(BaseModel):

    email: EmailStr

    cover_letter: str


# ==========================================
# RESPONSE
# ==========================================

class JobApplicationResponse(BaseModel):

    id: int

    job_id: int

    email: EmailStr

    cover_letter: str

    resume_url: str

    status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# UPDATE APPLICATION STATUS
# ==========================================

class JobApplicationStatusUpdate(BaseModel):

    status: str