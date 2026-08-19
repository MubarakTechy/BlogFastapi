from sqlalchemy.orm import Session

from app.models import Contact
from app.contact.schema import ContactCreate


def create_contact(db: Session, data: ContactCreate):

    contact = Contact(
        full_name=data.full_name,
        email=data.email,
        message=data.message,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact