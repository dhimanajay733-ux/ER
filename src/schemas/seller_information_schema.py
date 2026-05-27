from pydantic import BaseModel


class CreateSellerInformation(BaseModel):

    user_id: str
    store_name: str


class UpdateSellerInformation(BaseModel):

    store_name: str | None = None
    status: bool | None = None