from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str | None = None
    sub_category_id: int
    seller_id: int
    size: str | None = None
    color: str | None = None
    image_link: str | None = None
    quantity: int