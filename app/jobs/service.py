from sqlalchemy.orm import Session

from app.models import Job
from app.jobs.schemas import JobCreate, JobUpdate


def create_job(
    db: Session,
    job_data: JobCreate,
    author_id: int
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        description=job_data.description,
        requirements=job_data.requirements,
        salary=job_data.salary,
        job_type=job_data.job_type,
        is_active=job_data.is_active,
        author_id=author_id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_jobs(db: Session):
    return db.query(Job).all()


def get_job_by_id(
    db: Session,
    job_id: int
):
    return db.query(Job).filter(Job.id == job_id).first()


def update_job(
    db: Session,
    job: Job,
    job_data: JobUpdate
):
    update_data = job_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    db: Session,
    job: Job
):
    db.delete(job)
    db.commit()