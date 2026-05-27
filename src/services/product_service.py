from sqlalchemy.orm import Session

from src.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)

from src.repository.products_repository import (

    create_product as create_product_repository,

    get_products as get_products_repository,

    search_products as search_products_repository,

    get_product_by_id as get_product_by_id_repository,

    update_product as update_product_repository,

    delete_product as delete_product_repository
)


# CREATE PRODUCT
def create_product(
    db: Session,
    payload: ProductCreate
):

    product = create_product_repository(
        db=db,
        payload=payload
    )

    db.commit()

    return product


# GET ALL PRODUCTS
def get_products(
    db: Session
):

    return get_products_repository(db)


# SEARCH PRODUCTS
def search_products(
    db: Session,
    search=None,
    subcategory_id=None,
    min_price=None,
    max_price=None
):

    return search_products_repository(

        db=db,

        search=search,

        subcategory_id=subcategory_id,

        min_price=min_price,

        max_price=max_price
    )

# GET PRODUCT BY ID
def get_product_by_id(
    db: Session,
    product_id: int
):

    return get_product_by_id_repository(
        db,
        product_id
    )

# UPDATE PRODUCT
def update_product(
    db: Session,
    product_id: int,
    payload: ProductUpdate
):

    product = get_product_by_id_repository(
        db,
        product_id
    )

    if not product:

        return None

    updated_product = update_product_repository(
        db,
        product,
        payload
    )

    db.commit()

    return updated_product


# DELETE PRODUCT
def delete_product(
    db: Session,
    product_id: int
):

    product = get_product_by_id_repository(
        db,
        product_id
    )

    if not product:

        return None

    delete_product_repository(
        db,
        product
    )

    db.commit()

    return True