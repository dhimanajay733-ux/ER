from sqlalchemy.orm import Session

from src.models.products_model import Product
from src.models.subcategory_model import SubCategory
from src.models.category_model import Category
from src.core.logger import logger
from src.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)
from src.utils import generate_slug

from src.schemas.product_schema import (
    ProductFilter
)

from src.exceptions.database_exception import (
    DatabaseInsertException,
    DatabaseFetchException,
    DatabaseUpdateException
)


# CREATE PRODUCT
def create_product(
    db: Session,
    payload: ProductCreate
):

    try:
        slug = generate_slug(
            db,
            Product,
            payload.name
        )

        new_product = Product(
        
        name=payload.name,

        slug=slug,

        price=payload.price,

        description=payload.description,

        sub_category_id=payload.sub_category_id,

        seller_id=payload.seller_id,

        size=payload.size,

        color=payload.color,

        image_link=payload.image_link,

        quantity=payload.quantity
                )

            
        db.add(new_product)

        db.flush()

        db.refresh(new_product)

        return new_product
    except Exception as e:

        logger.error(
        f"Failed to create product: {str(e)}"
    )
        
        raise DatabaseInsertException(
            str(e)
        )
    
# GET ALL PRODUCTS
def get_products(
    db: Session
):

    try:

        query = db.query(Product)

        products = query.all()

        return products

    except Exception as e:

        logger.error(
            f"Failed to fetch products: {str(e)}"
        )

        raise DatabaseFetchException(
            str(e)
        )

# SEARCH PRODUCTS
def search_products(
    db: Session,
    filters: ProductFilter
):

    try:

        query = db.query(Product)

        # SEARCH BY PRODUCT NAME
        if (
            filters.search
            and filters.search.strip()
            and filters.search != "string"
        ):

            query = query.filter(
                Product.name.ilike(
                    f"%{filters.search.strip()}%"
                )
            )

        # FILTER BY CATEGORY
        if (
            filters.category_type
            and filters.category_type.strip()
            and filters.category_type != "string"
        ):

            query = (
                query
                .join(SubCategory)
                .join(Category)
                .filter(
                    Category.type.ilike(
                        f"%{filters.category_type.strip()}%"
                    )
                )
            )

        # FILTER BY SUBCATEGORY
        if (
            filters.subcategory_id is not None
            and filters.subcategory_id > 0
        ):

            query = query.filter(
                Product.sub_category_id
                == filters.subcategory_id
            )

        # FILTER BY MIN PRICE
        if (
            filters.min_price is not None
            and filters.min_price > 0
        ):

            query = query.filter(
                Product.price >= filters.min_price
            )

        # FILTER BY MAX PRICE
        if (
            filters.max_price is not None
            and filters.max_price > 0
        ):

            query = query.filter(
                Product.price <= filters.max_price
            )

        # FILTER BY COLOR
        if (
            filters.color
            and filters.color.strip()
            and filters.color != "string"
        ):

            query = query.filter(
                Product.color.ilike(
                    f"%{filters.color.strip()}%"
                )
            )

        # FILTER BY SIZE
        if (
            filters.size
            and filters.size.strip()
            and filters.size != "string"
        ):

            query = query.filter(
                Product.size.ilike(
                    f"%{filters.size.strip()}%"
                )
            )

        # FILTER STOCK STATUS
        if filters.stock_status == "in_stock":

            query = query.filter(
                Product.quantity > 0
            )

        elif filters.stock_status == "out_of_stock":

            query = query.filter(
                Product.quantity == 0
            )

        products = query.all()

        return products

    except Exception as e:

        logger.error(
            f"Failed to search products: {str(e)}"
        )

        raise DatabaseFetchException(
            str(e)
        )

# GET PRODUCT BY ID
def get_product_by_id(
    db: Session,
    product_id: int
):

    try:

        query = (
            db.query(Product)
            .filter(Product.id == product_id)
        )

        product = query.first()

        return product

    except Exception as e:

        logger.error(
            f"failed to get product by id: {str(e)}"
        )

        raise DatabaseFetchException(
            str(e)
        )

def update_product(
    db: Session,
     product: Product,
     payload: ProductUpdate
):

    try:

        if payload.name is not None:

            product.name = payload.name

            product.slug = generate_slug(
                db,
                Product,
                payload.name
            )

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

    except Exception as e:

        logger.error(
            f"Failed to update product: {str(e)}"
        )

        raise DatabaseUpdateException(
            str(e)
        )

# DELETE PRODUCT
def delete_product(
    db: Session,
    product: Product
):
    
    try:

        db.delete(product)

        db.flush()

        return True

    except Exception as e:

        raise e
    

def get_product_by_slug(
    db: Session,
    slug: str
):

    try:

        query = (
            db.query(Product)
            .filter(Product.slug == slug)
        )

        product = query.first()

        return product

    except Exception as e:

        logger.error(
            f"Failed to fetch product by slug: {str(e)}"
        )

        raise DatabaseFetchException(
            str(e)
        )