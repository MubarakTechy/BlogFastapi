from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.contact.schema import ContactCreate, ContactResponse
from app.contact.service import create_contact


router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


@router.post("/", response_model=ContactResponse)
def submit_contact(
    data: ContactCreate,
    db: Session = Depends(get_db)
):
    return create_contact(db, data)