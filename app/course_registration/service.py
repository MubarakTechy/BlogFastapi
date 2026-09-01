from sqlalchemy.orm import Session

from app.models import CourseRegistration
from app.course_registration.schemas import (
    CourseRegistrationCreate
)


# ==========================================
# CREATE REGISTRATION
# ==========================================

def create_registration(
    db: Session,
    registration_data: CourseRegistrationCreate
):

    registration = CourseRegistration(
        full_name=registration_data.full_name,
        email=registration_data.email,
        course=registration_data.course,
        city=registration_data.city,
        state=registration_data.state,
        other=registration_data.other,
        reason=registration_data.reason
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


# ==========================================
# GET ALL REGISTRATIONS
# ==========================================

def get_registrations(db: Session):

    return db.query(
        CourseRegistration
    ).order_by(
        CourseRegistration.created_at.desc()
    ).all()


# ==========================================
# GET ONE REGISTRATION
# ==========================================

def get_registration_by_id(
    db: Session,
    registration_id: int
):

    return db.query(
        CourseRegistration
    ).filter(
        CourseRegistration.id == registration_id
    ).first()


# ==========================================
# DELETE REGISTRATION
# ==========================================

def delete_registration(
    db: Session,
    registration: CourseRegistration
):

    db.delete(registration)
    db.commit()