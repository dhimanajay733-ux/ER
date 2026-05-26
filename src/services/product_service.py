from src.models.products_model import Product


def create_product(db, payload):

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

    db.commit()

    db.refresh(product)

    return product


def get_products(db):

    return db.query(Product).all()


def get_product_by_id(db, product_id):

    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def update_product(db, product_id, payload):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return None

    product.name = payload.name
    product.price = payload.price
    product.description = payload.description
    product.quantity = payload.quantity

    db.commit()

    db.refresh(product)

    return product


def delete_product(db, product_id):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return None

    db.delete(product)

    db.commit()

    return True