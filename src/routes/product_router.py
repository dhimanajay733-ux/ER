from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from src.db.session_db import get_db
from src.schemas.product_schema import ProductCreate

from src.services.product_service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/")
def create_product_api(
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(
        db=db,
        payload=payload
    )


@router.get("/")
def get_products_api(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get("/product_id")
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


@router.put("/product_id")
def update_product_api(
    product_id: int,
    payload: ProductCreate,
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


@router.delete("/product_id")
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