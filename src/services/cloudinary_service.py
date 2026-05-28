import cloudinary.uploader

from src.core.logger import logger


def upload_product_image(
    file
):

    try:

        logger.info(
            "Uploading product image to Cloudinary"
        )

        result = cloudinary.uploader.upload(file)

        image_url = result["secure_url"]

        logger.info(
            f"Image uploaded successfully: {image_url}"
        )

        return image_url

    except Exception as e:

        logger.error(
            f"Cloudinary upload failed: {str(e)}"
        )

        raise e