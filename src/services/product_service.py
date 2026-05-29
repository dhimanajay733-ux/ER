from sqlalchemy.orm import Session

from src.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)
from src.schemas.product_schema import (
    ProductFilter
)

from src.repository.products_repository import (

    create_product as create_product_repository,

    get_products as get_products_repository,

    search_products as search_products_repository,

    get_product_by_id as get_product_by_id_repository,

    update_product as update_product_repository,

    delete_product as delete_product_repository,

    get_product_by_slug 
)
from src.exceptions.common_exception import (
    NotFoundException
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
# def create_products(
#     db: Session,
#     payload: list[ProductCreate]
# ):

#     products = []

#     for product_data in payload:

#         product = create_product_repository(
#             db=db,
#             payload=product_data
#         )

#         products.append(product)

#     db.commit()

#     return products

# GET ALL PRODUCTS
def get_products(
    db: Session
):

    return get_products_repository(db)

# SEARCH PRODUCTS
def search_products(
    db: Session,
    filters: ProductFilter
):

    return search_products_repository(
        db=db,
        filters=filters
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

#Get product by slug
def fetch_product_by_slug(
    db: Session,
    slug: str
):

    product = get_product_by_slug(
        db,
        slug
    )

    if not product:

        raise NotFoundException(
            "Product not found"
        )

    return product