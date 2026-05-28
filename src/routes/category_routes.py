from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from src.db.session_db import get_db

from src.schemas.category_schema import (
    CreateCategory,
    UpdateCategory
)

from src.services.categories_service import (
    generate_category,
    fetch_all_categories,
    fetch_single_category,
    modify_category,
    remove_category
)

from src.exceptions.common_exception import (
    AlreadyExistsException,
    NotFoundException
)

from src.core.logger import logger

router = APIRouter(
    prefix="/api/categories",
    tags=["Category"]
)


# CREATE CATEGORY
@router.post("/")
def create_category_route(
    user_data: CreateCategory,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Received create category request: {user_data.type}"
    )

    try:

        category = generate_category(
            db=db,
            data=user_data
        )

        logger.info(
            f"Category created successfully: {category.id}"
        )

        return category

    except AlreadyExistsException as e:

        logger.warning(
            f"Category already exists: {user_data.type}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# GET ALL CATEGORIES
@router.get("/")
def get_all_categories_route(
    db: Session = Depends(get_db)
):

    logger.info(
        "Fetching all categories"
    )

    return fetch_all_categories(db)


# GET SINGLE CATEGORY
@router.get("/{category_id}")
def get_single_category_route(
    category_id: str,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Fetching category: {category_id}"
    )

    try:

        return fetch_single_category(
            db,
            category_id
        )

    except NotFoundException as e:

        logger.warning(
            f"Category not found: {category_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# UPDATE CATEGORY
@router.put("/{category_id}")
def update_category_route(
    category_id: str,
    user_data: UpdateCategory,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Updating category: {category_id}"
    )

    try:

        updated_category = modify_category(
            db=db,
            category_id=category_id,
            data=user_data
        )

        logger.info(
            f"Category updated successfully: {category_id}"
        )

        return updated_category

    except NotFoundException as e:

        logger.warning(
            f"Category not found for update: {category_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# DELETE CATEGORY
@router.delete("/{category_id}")
def delete_category_route(
    category_id: str,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Deleting category: {category_id}"
    )

    try:

        response = remove_category(
            db,
            category_id
        )

        logger.info(
            f"Category deleted successfully: {category_id}"
        )

        return response

    except NotFoundException as e:

        logger.warning(
            f"Category not found for deletion: {category_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )