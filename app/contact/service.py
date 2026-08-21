from sqlalchemy.orm import Session

from app.models import Contact
from app.contact.schema import ContactCreate


def create_contact(
    db: Session,
    data: ContactCreate
):
    contact = Contact(
        full_name=data.full_name,
        email=data.email,
        message=data.message
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_all_contacts(db: Session):
    return db.query(Contact).order_by(
        Contact.created_at.desc()
    ).all()


def delete_contact(
    db: Session,
    contact_id: int
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id
    ).first()

    if not contact:
        return None

    db.delete(contact)
    db.commit()

    return contact