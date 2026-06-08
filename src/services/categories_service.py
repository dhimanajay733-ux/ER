from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
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

from src.core.logger import logger


# CREATE CATEGORY
async def generate_category(
    db: AsyncSession,
    data: CreateCategory
):

    logger.info(
        f"Checking existing category: {data.type}"
    )

    existing_category = await get_category_by_type(
        db,
        data.type
    )

    if existing_category:

        logger.warning(
            f"Category already exists: {data.type}"
        )

        raise AlreadyExistsException(
            "Category already exists"
        )

    try:

        logger.info(
            f"Creating category: {data.type}"
        )

        new_category = await create_category(
            db=db,
            data=data
        )

        await db.commit()

        logger.info(
            f"Category committed successfully: {new_category.id}"
        )

        return new_category

    except Exception as e:

        db.rollback()

        logger.error(
            f"Category creation failed: {str(e)}"
        )

        raise e


# GET ALL CATEGORIES
async def fetch_all_categories(
    db: AsyncSession
):

    logger.info(
        "Fetching all categories from database"
    )

    return await  get_all_categories(db)


# GET SINGLE CATEGORY
async def fetch_single_category(
    db: AsyncSession,
    category_id: str
):

    logger.info(
        f"Fetching category by id: {category_id}"
    )

    category = await get_category_by_id(
        db,
        category_id
    )

    if not category:

        logger.warning(
            f"Category not found: {category_id}"
        )

        raise NotFoundException(
            "Category not found"
        )

    return  category


# UPDATE CATEGORY
async def modify_category(
    db: AsyncSession,
    category_id: str,
    data: UpdateCategory
):

    logger.info(
        f"Checking category before update: {category_id}"
    )

    category = await get_category_by_id(
        db,
        category_id
    )

    if not category:

        logger.warning(
            f"Category not found for update: {category_id}"
        )

        raise NotFoundException(
            "Category not found"
        )

    try:

        logger.info(
            f"Updating category: {category_id}"
        )

        updated_category = await update_category(
            db=db,
            category=category,
            data=data
        )

        await db.commit()

        logger.info(
            f"Category updated successfully: {category_id}"
        )

        return updated_category

    except Exception as e:

        db.rollback()

        logger.error(
            f"Category update failed: {str(e)}"
        )

        raise e


# DELETE CATEGORY
def remove_category(
    db: Session,
    category_id: str
):

    logger.info(
        f"Checking category before deletion: {category_id}"
    )

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:

        logger.warning(
            f"Category not found for deletion: {category_id}"
        )

        raise NotFoundException(
            "Category not found"
        )

    try:

        logger.info(
            f"Deleting category: {category_id}"
        )

        delete_category(
            db,
            category
        )

        db.commit()

        logger.info(
            f"Category deleted successfully: {category_id}"
        )

        return {
            "message": "Category deleted successfully"
        }

    except Exception as e:

        db.rollback()

        logger.error(
            f"Category deletion failed: {str(e)}"
        )

        raise e