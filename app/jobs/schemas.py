from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: str
    salary: str | None = None
    job_type: str
    is_active: bool = True


class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    description: str | None = None
    requirements: str | None = None
    salary: str | None = None
    job_type: str | None = None
    is_active: bool | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    requirements: str
    salary: str | None
    job_type: str
    is_active: bool
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)