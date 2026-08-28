from io import BytesIO

from PIL import Image
import cloudinary.uploader


def upload_image(file):

    image = Image.open(file)
    image.verify()

    file.seek(0)

    result = cloudinary.uploader.upload(
        file,
        folder="blog_images"
    )

    return result["secure_url"]