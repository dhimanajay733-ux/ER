from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from src.db.session_db import get_db

from src.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
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


# CREATE PRODUCT
@router.post("/")
def create_product_api(

    name: str = Form(...),

    price: float = Form(...),

    description: str = Form(...),

    sub_category_id: int = Form(...),

    seller_id: str = Form(...),

    quantity: int = Form(...),

    size: str | None = Form(None),

    color: str | None = Form(None),

    image: UploadFile = File(...),

    db: Session = Depends(get_db)
):

    image_url = upload_product_image(
        image.file
    )

    payload = ProductCreate(

        name=name,

        price=price,

        description=description,

        sub_category_id=sub_category_id,

        seller_id=seller_id,

        quantity=quantity,

        size=size,

        color=color,

        image_link=image_url
    )

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
@router.get("/search/")
def search_products_api(

    search: str | None = None,

    subcategory_id: int | None = None,

    min_price: float | None = None,

    max_price: float | None = None,

    db: Session = Depends(get_db)
):

    return search_products(

        db=db,

        search=search,

        subcategory_id=subcategory_id,

        min_price=min_price,

        max_price=max_price
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