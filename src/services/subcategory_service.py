from sqlalchemy.orm import Session

from src.schemas.subcategory_schema import (
    CreateSubCategory,
    UpdateSubCategory
)

from src.repository.subcategory_repository import (
    create_subcategory,
    get_subcategory_by_id,
    get_subcategory_by_type,
    get_all_subcategories,
    update_subcategory,
    delete_subcategory
)

from src.repository.category_repository import (
    get_category_by_id
)

from src.exceptions.common_exception import (
    AlreadyExistsException,
    NotFoundException
)


# CREATE SUBCATEGORY
def generate_subcategory(
    db: Session,
    data: CreateSubCategory
):

    # CHECK CATEGORY EXISTS
    category = get_category_by_id(
        db,
        data.category_id
    )

    if not category:

        raise NotFoundException(
            "Category not found"
        )

    # CHECK SUBCATEGORY EXISTS
    existing_subcategory = get_subcategory_by_type(
        db,
        data.type
    )

    if existing_subcategory:

        raise AlreadyExistsException(
            "Subcategory already exists"
        )

    try:

        new_subcategory = create_subcategory(
            db=db,
            data=data
        )

        db.commit()

        return new_subcategory

    except Exception as e:

        db.rollback()

        raise e


# GET ALL SUBCATEGORIES
def fetch_all_subcategories(
    db: Session
):

    return get_all_subcategories(db)


# GET SINGLE SUBCATEGORY
def fetch_single_subcategory(
    db: Session,
    subcategory_id: str
):

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    if not subcategory:

        raise NotFoundException(
            "Subcategory not found"
        )

    return subcategory


# UPDATE SUBCATEGORY
def modify_subcategory(
    db: Session,
    subcategory_id: str,
    data: UpdateSubCategory
):

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    if not subcategory:

        raise NotFoundException(
            "Subcategory not found"
        )

    try:

        updated_subcategory = update_subcategory(
            db=db,
            subcategory=subcategory,
            data=data
        )

        db.commit()

        return updated_subcategory

    except Exception as e:

        db.rollback()

        raise e


# DELETE SUBCATEGORY
def remove_subcategory(
    db: Session,
    subcategory_id: str
):

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    if not subcategory:

        raise NotFoundException(
            "Subcategory not found"
        )

    try:

        delete_subcategory(
            db,
            subcategory
        )

        db.commit()

        return {
            "message": "Subcategory deleted successfully"
        }

    except Exception as e:

        db.rollback()

        raise e