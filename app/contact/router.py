from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Contact

from app.contact.schema import (
    ContactCreate,
    ContactResponse
)

from app.contact.service import (
    create_contact,
    get_all_contacts,
    delete_contact
)

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


# ==========================================
# PUBLIC - Submit Contact Message
# ==========================================

@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_contact(
    data: ContactCreate,
    db: Session = Depends(get_db)
):
    return create_contact(
        db,
        data
    )


# ==========================================
# ADMIN ONLY - View Contacts
# ==========================================

@router.get(
    "/",
    response_model=list[ContactResponse]
)
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return get_all_contacts(db)


# ==========================================
# ADMIN ONLY - Delete Contact
# ==========================================

@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    contact = delete_contact(
        db,
        contact_id
    )

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found"
        )

    return None