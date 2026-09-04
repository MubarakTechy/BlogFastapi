from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.dependencies import get_current_admin
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.utils.resume_upload import upload_resume
from app.models import Job, Admin

from app.job_applications.schemas import (
    JobApplicationResponse,
    JobApplicationStatusUpdate
)

from app.job_applications.service import (
    create_application,
    get_all_applications,
    get_application_by_id,
    get_applications_for_job,
    update_application_status,
    delete_application
)

from app.utils.resume_upload import upload_resume


router = APIRouter(
    prefix="/jobs",
    tags=["Job Applications"]
)


# ==========================================
# APPLY FOR JOB
# PUBLIC
# ==========================================
@router.post(
    "/{job_id}/apply",
    response_model=JobApplicationResponse,
    status_code=201
)
def apply_for_job(
    job_id: int,
    email: str = Form(...),
    cover_letter: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if not job.is_active:
        raise HTTPException(
            status_code=400,
            detail="This job is no longer accepting applications"
        )

    try:
        resume_url = upload_resume(
            resume.file,
            resume.filename
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        print("RESUME UPLOAD ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Resume upload failed"
        )

    return create_application(
        db=db,
        job=job,
        email=email,
        cover_letter=cover_letter,
        resume_url=resume_url
    )
    # --------------------------------------
    # FIND JOB
    # --------------------------------------

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # --------------------------------------
    # CHECK IF JOB IS ACTIVE
    # --------------------------------------

    if not job.is_active:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This job is no longer accepting applications"
        )

    # --------------------------------------
    # UPLOAD CV
    # --------------------------------------

    try:

        resume_url = upload_resume(
            resume.file
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resume upload failed"
        )

    # --------------------------------------
    # CREATE APPLICATION
    # --------------------------------------

    application = create_application(
        db=db,
        job=job,
        email=email,
        cover_letter=cover_letter,
        resume_url=resume_url
    )

    return application


# ==========================================
# GET ALL APPLICATIONS
# ADMIN ONLY
# ==========================================

@router.get("/applications", response_model=list[JobApplicationResponse])
def get_all_job_applications(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    return get_all_applications(db)


@router.get("/{job_id}/applications", response_model=list[JobApplicationResponse])
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return get_applications_for_job(db, job_id)

# ==========================================
# GET ONE APPLICATION
# ADMIN ONLY
# ==========================================

@router.get(
    "/applications/{application_id}",
    response_model=JobApplicationResponse
)
def get_single_application(

    application_id: int,

    db: Session = Depends(get_db),

    admin: Admin = Depends(get_current_admin)

):

    application = get_application_by_id(
        db,
        application_id
    )

    if not application:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application


# ==========================================
# UPDATE APPLICATION STATUS
# ADMIN ONLY
# ==========================================

@router.put(
    "/applications/{application_id}",
    response_model=JobApplicationResponse
)
def update_job_application(

    application_id: int,

    application_data: JobApplicationStatusUpdate,

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)

):

    application = get_application_by_id(
        db,
        application_id
    )

    if not application:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    allowed_statuses = {
        "Pending",
        "Reviewed",
        "Shortlisted",
        "Rejected",
        "Accepted"
    }

    if application_data.status not in allowed_statuses:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid status. Choose from: "
                "Pending, Reviewed, Shortlisted, "
                "Rejected, Accepted"
            )
        )

    return update_application_status(
        db,
        application,
        application_data.status
    )


# ==========================================
# DELETE APPLICATION
# ADMIN ONLY
# ==========================================

@router.delete(
    "/applications/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_job_application(

    application_id: int,

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)

):

    application = get_application_by_id(
        db,
        application_id
    )

    if not application:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    delete_application(
        db,
        application
    )

    return None