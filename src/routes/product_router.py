from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)
from src.core.logger import logger
from sqlalchemy.orm import Session

from src.db.session_db import get_db

from src.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)

from src.schemas.product_schema import (
    ProductFilter
)

from src.services.product_service import (
    create_product,
    get_products,
    search_products,
    get_product_by_id,
    update_product,
    delete_product
)

from src.services.cloudinary_service import (
    upload_product_image
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# UPLOAD IMAGE
@router.post("/upload-image")
def upload_product_image_api(
    image: UploadFile = File(...)
):

    logger.info(
        f"Received image upload request: {image.filename}"
    )

    image_url = upload_product_image(
        image.file
    )

    logger.info(
        f"Returning uploaded image URL: {image_url}"
    )

    return {
        "image_url": image_url
    }


# CREATE PRODUCT
@router.post("/")
def create_product_api(
    payload: ProductCreate,
    db: Session = Depends(get_db)
):

    return create_product(
        db=db,
        payload=payload
    )


# GET ALL PRODUCTS
@router.get("/")
def get_products_api(
    db: Session = Depends(get_db)
):

    return get_products(db)


# SEARCH PRODUCTS
@router.post("/search/")
def search_products_api(

    filters: ProductFilter,

    db: Session = Depends(get_db)
):

    return search_products(
        db=db,
        filters=filters
    )


# GET PRODUCT BY ID
@router.get("/{product_id}")
def get_product_by_id_api(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = get_product_by_id(
        db,
        product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# UPDATE PRODUCT
@router.put("/{product_id}")
def update_product_api(

    product_id: int,

    payload: ProductUpdate,

    db: Session = Depends(get_db)
):

    product = update_product(
        db,
        product_id,
        payload
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# DELETE PRODUCT
@router.delete("/{product_id}")
def delete_product_api(
    product_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_product(
        db,
        product_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }