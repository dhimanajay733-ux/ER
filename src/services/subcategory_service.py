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

from src.core.logger import logger


# CREATE SUBCATEGORY
async def generate_subcategory(
    db: Session,
    data: CreateSubCategory
):

    logger.info(
        f"Checking category existence: {data.category_id}"
    )

    # CHECK CATEGORY EXISTS
    category = await get_category_by_id(
        db,
        data.category_id
    )

    if not category:

        logger.warning(
            f"Category not found: {data.category_id}"
        )

        raise NotFoundException(
            "Category not found"
        )

    logger.info(
        f"Checking existing subcategory: {data.type}"
    )

    # CHECK SUBCATEGORY EXISTS
    existing_subcategory = await get_subcategory_by_type(
        db,
        data.type
    )

    if await existing_subcategory:

        logger.warning(
            f"Subcategory already exists: {data.type}"
        )

        raise AlreadyExistsException(
            "Subcategory already exists"
        )

    try:

        logger.info(
            f"Creating subcategory: {data.type}"
        )

        new_subcategory = await create_subcategory(
            db=db,
            data=data
        )

        db.commit()

        logger.info(
            f"Subcategory committed successfully: {new_subcategory.id}"
        )

        return new_subcategory

    except Exception as e:

        db.rollback()

        logger.error(
            f"Subcategory creation failed: {str(e)}"
        )

        raise e


# GET ALL SUBCATEGORIES
async def fetch_all_subcategories(
    db: Session
):

    logger.info(
        "Fetching all subcategories from database"
    )

    return get_all_subcategories(db)


# GET SINGLE SUBCATEGORY
def fetch_single_subcategory(
    db: Session,
    subcategory_id: str
):

    logger.info(
        f"Fetching subcategory by id: {subcategory_id}"
    )

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    if not subcategory:

        logger.warning(
            f"Subcategory not found: {subcategory_id}"
        )

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

    logger.info(
        f"Checking subcategory before update: {subcategory_id}"
    )

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    if not subcategory:

        logger.warning(
            f"Subcategory not found for update: {subcategory_id}"
        )

        raise NotFoundException(
            "Subcategory not found"
        )

    try:

        logger.info(
            f"Updating subcategory: {subcategory_id}"
        )

        updated_subcategory = update_subcategory(
            db=db,
            subcategory=subcategory,
            data=data
        )

        db.commit()

        logger.info(
            f"Subcategory updated successfully: {subcategory_id}"
        )

        return updated_subcategory

    except Exception as e:

        db.rollback()

        logger.error(
            f"Subcategory update failed: {str(e)}"
        )

        raise e


# DELETE SUBCATEGORY
def remove_subcategory(
    db: Session,
    subcategory_id: str
):

    logger.info(
        f"Checking subcategory before deletion: {subcategory_id}"
    )

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    if not subcategory:

        logger.warning(
            f"Subcategory not found for deletion: {subcategory_id}"
        )

        raise NotFoundException(
            "Subcategory not found"
        )

    try:

        logger.info(
            f"Deleting subcategory: {subcategory_id}"
        )

        delete_subcategory(
            db,
            subcategory
        )

        db.commit()

        logger.info(
            f"Subcategory deleted successfully: {subcategory_id}"
        )

        return {
            "message": "Subcategory deleted successfully"
        }

    except Exception as e:

        db.rollback()

        logger.error(
            f"Subcategory deletion failed: {str(e)}"
        )

        raise e