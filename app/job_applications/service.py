from sqlalchemy.orm import Session

from app.models import (
    Job,
    JobApplication
)


# ==========================================
# CREATE APPLICATION
# ==========================================

def create_application(
    db: Session,
    job: Job,
    email: str,
    cover_letter: str,
    resume_url: str
):

    application = JobApplication(
        job_id=job.id,
        email=email,
        cover_letter=cover_letter,
        resume_url=resume_url,
        status="Pending"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


# ==========================================
# GET ALL APPLICATIONS
# ==========================================

def get_all_applications(
    db: Session
):

    return db.query(
        JobApplication
    ).order_by(
        JobApplication.created_at.desc()
    ).all()


# ==========================================
# GET APPLICATION BY ID
# ==========================================

def get_application_by_id(
    db: Session,
    application_id: int
):

    return db.query(
        JobApplication
    ).filter(
        JobApplication.id == application_id
    ).first()


# ==========================================
# GET APPLICATIONS FOR A JOB
# ==========================================

def get_applications_for_job(
    db: Session,
    job_id: int
):

    return db.query(
        JobApplication
    ).filter(
        JobApplication.job_id == job_id
    ).order_by(
        JobApplication.created_at.desc()
    ).all()


# ==========================================
# UPDATE APPLICATION STATUS
# ==========================================

def update_application_status(
    db: Session,
    application: JobApplication,
    new_status: str
):

    application.status = new_status

    db.commit()
    db.refresh(application)

    return application


# ==========================================
# DELETE APPLICATION
# ==========================================

def delete_application(
    db: Session,
    application: JobApplication
):

    db.delete(application)
    db.commit()