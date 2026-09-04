import uuid
import cloudinary.uploader


ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def upload_resume(file, filename: str):
    extension = ""

    if filename and "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF, DOC, and DOCX files are allowed"
        )

    public_id = f"{uuid.uuid4().hex}{extension}"

    result = cloudinary.uploader.upload(
        file,
        resource_type="raw",
        folder="job_resumes",
        public_id=public_id
    )

    return result["secure_url"]