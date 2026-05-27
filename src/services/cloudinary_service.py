import cloudinary.uploader


def upload_product_image(
    file
):

    response = cloudinary.uploader.upload(file)

    return response["secure_url"]