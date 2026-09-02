import cloudinary.uploader


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx"
}


def upload_resume(file):

    filename = file.filename or ""
    extension = ""

    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF, DOC, and DOCX files are allowed"
        )

    result = cloudinary.uploader.upload(
        file,
        folder="job_resumes",
        resource_type="raw"
    )

    return result["secure_url"]