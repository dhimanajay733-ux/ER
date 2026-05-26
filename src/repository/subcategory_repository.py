from sqlalchemy.orm import Session

from src.models.subcategory_model import (
    SubCategory
)

from src.schemas.subcategory_schema import (
    CreateSubCategory,
    UpdateSubCategory
)


# CREATE SUBCATEGORY
def create_subcategory(
    db: Session,
    data: CreateSubCategory
):

    new_subcategory = SubCategory(

        category_id=data.category_id,

        type=data.type,

        description=data.description
    )

    db.add(new_subcategory)

    db.flush()

    db.refresh(new_subcategory)

    return new_subcategory


# GET SUBCATEGORY BY ID
def get_subcategory_by_id(
    db: Session,
    subcategory_id: str
):

    return (
        db.query(SubCategory)
        .filter(SubCategory.id == subcategory_id)
        .first()
    )


# GET SUBCATEGORY BY TYPE
def get_subcategory_by_type(
    db: Session,
    type: str
):

    return (
        db.query(SubCategory)
        .filter(SubCategory.type == type)
        .first()
    )


# GET ALL SUBCATEGORIES
def get_all_subcategories(
    db: Session
):

    return db.query(SubCategory).all()


# UPDATE SUBCATEGORY
def update_subcategory(
    db: Session,
    subcategory: SubCategory,
    data: UpdateSubCategory
):

    if data.type is not None:

        subcategory.type = data.type

    if data.description is not None:

        subcategory.description = data.description

    db.add(subcategory)

    db.flush()

    db.refresh(subcategory)

    return subcategory


# DELETE SUBCATEGORY
def delete_subcategory(
    db: Session,
    subcategory: SubCategory
):

    db.delete(subcategory)

    db.flush()