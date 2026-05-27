from pydantic import BaseModel


class ProductCreate(BaseModel):

    name: str
    price: float
    description: str | None = None
    sub_category_id: int
    seller_id: str
    size: str | None = None
    color: str | None = None
    image_link: str | None = None
    quantity: int = 0


class ProductUpdate(BaseModel):

    name: str | None = None
    price: float | None = None
    description: str | None = None
    size: str | None = None
    color: str | None = None
    image_link: str | None = None
    quantity: int | None = None