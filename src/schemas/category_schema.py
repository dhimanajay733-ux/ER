from pydantic import BaseModel


class CreateCategory(BaseModel):

    type: str

    description: str | None = None


class UpdateCategory(BaseModel):

    type: str | None = None

    description: str | None = None