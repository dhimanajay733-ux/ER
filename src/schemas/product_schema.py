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

class ProductFilter(BaseModel):

    search: str | None = None
    category_type: str | None = None
    subcategory_id: int | None = None
    min_price: int | None = None
    max_price: int | None = None
    color: str | None = None
    size: str | None = None
    stock_status: str | None = None


