from sqlalchemy.orm import Session

from src.models.products_model import Product
from src.models.category_model import Category

from src.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)


# CREATE PRODUCT
def create_product(
    db: Session,
    payload: ProductCreate
):

    product = Product(

        name=payload.name,

        price=payload.price,

        description=payload.description,

        sub_category_id=payload.sub_category_id,

        seller_id=payload.seller_id,

        size=payload.size,

        color=payload.color,

        image_link=payload.image_link,

        quantity=payload.quantity
    )

    db.add(product)

    db.flush()

    db.refresh(product)

    return product


# GET ALL PRODUCTS
def get_products(
    db: Session
):

    return db.query(Product).all()


# SEARCH PRODUCTS
def search_products(
    db: Session,
    search=None,
    subcategory_id=None,
    min_price=None,
    max_price=None
):

    query = db.query(Product)

    # SEARCH BY NAME
    if search:

        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )
    # JOIN EXAMPLE
    if search:

        query =query.filter(
            Product
        ).join(Category)

    # FILTER BY SUBCATEGORY
    if subcategory_id:

        query = query.filter(
            Product.sub_category_id == subcategory_id
        )

    # FILTER BY MIN PRICE
    if min_price:

        query = query.filter(
            Product.price >= min_price
        )

    # FILTER BY MAX PRICE
    if max_price:

        query = query.filter(
            Product.price <= max_price
        )
    
    return query.all()


# GET PRODUCT BY ID
def get_product_by_id(
    db: Session,
    product_id: int
):

    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


# UPDATE PRODUCT
def update_product(
    db: Session,
    product: Product,
    payload: ProductUpdate
):

    if payload.name is not None:

        product.name = payload.name

    if payload.price is not None:

        product.price = payload.price

    if payload.description is not None:

        product.description = payload.description

    if payload.size is not None:

        product.size = payload.size

    if payload.color is not None:

        product.color = payload.color

    if payload.image_link is not None:

        product.image_link = payload.image_link

    if payload.quantity is not None:

        product.quantity = payload.quantity

    db.add(product)

    db.flush()

    db.refresh(product)

    return product


# DELETE PRODUCT
def delete_product(
    db: Session,
    product: Product
):

    db.delete(product)

    db.flush()