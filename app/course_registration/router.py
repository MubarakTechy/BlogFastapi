from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.dependencies import get_current_admin

from app.course_registration.schemas import (
    CourseRegistrationCreate,
    CourseRegistrationResponse
)

from app.course_registration.service import (
    create_registration,
    get_registrations,
    get_registration_by_id,
    delete_registration
)


router = APIRouter(
    prefix="/course-registrations",
    tags=["Course Registrations"]
)


# ==========================================
# REGISTER FOR COURSE
# PUBLIC
# ==========================================

@router.post(
    "",
    response_model=CourseRegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register_for_course(
    registration_data: CourseRegistrationCreate,
    db: Session = Depends(get_db)
):

    return create_registration(
        db=db,
        registration_data=registration_data
    )


# ==========================================
# GET ALL REGISTRATIONS
# ADMIN ONLY
# ==========================================

@router.get(
    "",
    response_model=list[CourseRegistrationResponse]
)
def get_all_course_registrations(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return get_registrations(db)


# ==========================================
# GET ONE REGISTRATION
# ADMIN ONLY
# ==========================================

@router.get(
    "/{registration_id}",
    response_model=CourseRegistrationResponse
)
def get_single_registration(
    registration_id: int,

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)
):

    registration = get_registration_by_id(
        db,
        registration_id
    )

    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )

    return registration


# ==========================================
# DELETE REGISTRATION
# ADMIN ONLY
# ==========================================

@router.delete(
    "/{registration_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_course_registration(
    registration_id: int,

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)
):

    registration = get_registration_by_id(
        db,
        registration_id
    )

    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )

    delete_registration(
        db,
        registration
    )

    return None