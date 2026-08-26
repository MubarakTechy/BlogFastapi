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

from app.auth.dependencies import get_current_user

from app.jobs.schemas import (
    JobCreate,
    JobUpdate,
    JobResponse
)

from app.jobs.service import (
    create_job,
    get_jobs,
    get_job_by_id,
    update_job,
    delete_job
)

from app.utils.image_upload import upload_image


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# ==========================================
# CREATE JOB
# AUTHENTICATED USERS
# ==========================================

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_job(
    title: str = Form(...),
    company: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    requirements: str = Form(...),
    salary: str | None = Form(None),
    job_type: str = Form(...),
    is_active: bool = Form(True),
    image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)
):

    image_url = None

    # Upload image if provided
    if image:

        try:
            image_url = upload_image(
                image.file
            )

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Image upload failed"
            )

    job_data = JobCreate(
        title=title,
        company=company,
        location=location,
        description=description,
        requirements=requirements,
        salary=salary,
        job_type=job_type,
        is_active=is_active
    )

    return create_job(
        db=db,
        job_data=job_data,
        author_id=current_user.id,
        image_url=image_url
    )


# ==========================================
# GET ALL JOBS
# PUBLIC
# ==========================================

@router.get(
    "",
    response_model=list[JobResponse]
)
def get_all_jobs(
    db: Session = Depends(get_db)
):
    return get_jobs(db)


# ==========================================
# GET ONE JOB
# PUBLIC
# ==========================================

@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_single_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = get_job_by_id(
        db,
        job_id
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return job


# ==========================================
# UPDATE JOB
# AUTHENTICATED USERS
# ==========================================

@router.put(
    "/{job_id}",
    response_model=JobResponse
)
def update_existing_job(
    job_id: int,

    job_data: JobUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)
):

    job = get_job_by_id(
        db,
        job_id
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if not current_user.is_admin and job.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this job"
        )

    return update_job(
        db,
        job,
        job_data
    )


# ==========================================
# DELETE JOB
# AUTHENTICATED USERS
# ==========================================

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_job(
    job_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)
):

    job = get_job_by_id(
        db,
        job_id
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if not current_user.is_admin and job.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this job"
        )

    delete_job(
        db,
        job
    )

    return None