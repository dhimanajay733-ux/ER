from sqlalchemy.orm import Session

from src.db.session_db import SessionLocal
from src.models.products_model import Product
from src.utils import generate_slug

db: Session = SessionLocal()

products = db.query(Product).all()

for product in products:

    if not product.slug:

        product.slug = generate_slug(
            db,
            product.name
        )

db.commit()

print("Slugs generated successfully")