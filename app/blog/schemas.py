from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BlogCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class BlogUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    admin_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )