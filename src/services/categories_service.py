from sqlalchemy.orm import Session

from src.schemas.category_schema import (
    CreateCategory,
    UpdateCategory
)

from src.repository.category_repository import (
    create_category,
    get_category_by_id,
    get_category_by_type,
    get_all_categories,
    update_category,
    delete_category
)

from src.exceptions.common_exception import (
    AlreadyExistsException,
    NotFoundException
)


# CREATE CATEGORY
def generate_category(
    db: Session,
    data: CreateCategory
):

    existing_category = get_category_by_type(
        db,
        data.type
    )

    if existing_category:

        raise AlreadyExistsException(
            "Category already exists"
        )

    try:

        new_category = create_category(
            db=db,
            data=data
        )

        db.commit()

        return new_category

    except Exception as e:

        db.rollback()

        raise e


# GET ALL CATEGORIES
def fetch_all_categories(
    db: Session
):

    return get_all_categories(db)


# GET SINGLE CATEGORY
def fetch_single_category(
    db: Session,
    category_id: str
):

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:

        raise NotFoundException(
            "Category not found"
        )

    return category


# UPDATE CATEGORY
def modify_category(
    db: Session,
    category_id: str,
    data: UpdateCategory
):

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:

        raise NotFoundException(
            "Category not found"
        )

    try:

        updated_category = update_category(
            db=db,
            category=category,
            data=data
        )

        db.commit()

        return updated_category

    except Exception as e:

        db.rollback()

        raise e


# DELETE CATEGORY
def remove_category(
    db: Session,
    category_id: str
):

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:

        raise NotFoundException(
            "Category not found"
        )

    try:

        delete_category(
            db,
            category
        )

        db.commit()

        return {
            "message": "Category deleted successfully"
        }

    except Exception as e:

        db.rollback()

        raise e