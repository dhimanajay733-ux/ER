from pydantic import BaseModel


class CreateSubCategory(BaseModel):

    category_id: str
    type: str
    description: str | None = None


class UpdateSubCategory(BaseModel):

    type: str | None = None
    description: str | None = None