from sqlalchemy.orm import Session

from src.models.category_model import Category

from src.schemas.category_schema import (
    CreateCategory,
    UpdateCategory
)


# CREATE CATEGORY
def create_category(
    db: Session,
    data: CreateCategory
):

    new_category = Category(

        type=data.type,

        description=data.description
    )

    db.add(new_category)

    db.flush()

    db.refresh(new_category)

    return new_category


# GET CATEGORY BY ID
def get_category_by_id(
    db: Session,
    category_id: str
):

    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )


# GET CATEGORY BY TYPE
def get_category_by_type(
    db: Session,
    type: str
):

    return (
        db.query(Category)
        .filter(Category.type == type)
        .first()
    )


# GET ALL CATEGORIES
def get_all_categories(
    db: Session
):

    return db.query(Category).all()


# UPDATE CATEGORY
def update_category(
    db: Session,
    category: Category,
    data: UpdateCategory
):

    if data.type is not None:

        category.type = data.type

    if data.description is not None:

        category.description = data.description

    db.add(category)

    db.flush()

    db.refresh(category)

    return category


# DELETE CATEGORY
def delete_category(
    db: Session,
    category: Category
):

    db.delete(category)

    db.flush()