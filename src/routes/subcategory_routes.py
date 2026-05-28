from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from src.db.session_db import get_db

from src.schemas.subcategory_schema import (
    CreateSubCategory,
    UpdateSubCategory
)

from src.services.subcategory_service import (
    generate_subcategory,
    fetch_all_subcategories,
    fetch_single_subcategory,
    modify_subcategory,
    remove_subcategory
)

from src.exceptions.common_exception import (
    AlreadyExistsException,
    NotFoundException
)

from src.core.logger import logger

router = APIRouter(
    prefix="/api/subcategories",
    tags=["SubCategory"]
)


# CREATE SUBCATEGORY
@router.post("/")
def create_subcategory_route(
    user_data: CreateSubCategory,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Received create subcategory request: {user_data.type}"
    )

    try:

        subcategory = generate_subcategory(
            db=db,
            data=user_data
        )

        logger.info(
            f"Subcategory created successfully: {subcategory.id}"
        )

        return subcategory

    except AlreadyExistsException as e:

        logger.warning(
            f"Subcategory already exists: {user_data.type}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except NotFoundException as e:

        logger.warning(
            f"Parent category not found: {user_data.category_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# GET ALL SUBCATEGORIES
@router.get("/")
def get_all_subcategories_route(
    db: Session = Depends(get_db)
):

    logger.info(
        "Fetching all subcategories"
    )

    return fetch_all_subcategories(db)


# GET SINGLE SUBCATEGORY
@router.get("/{subcategory_id}")
def get_single_subcategory_route(
    subcategory_id: str,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Fetching subcategory: {subcategory_id}"
    )

    try:

        return fetch_single_subcategory(
            db,
            subcategory_id
        )

    except NotFoundException as e:

        logger.warning(
            f"Subcategory not found: {subcategory_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# UPDATE SUBCATEGORY
@router.put("/{subcategory_id}")
def update_subcategory_route(
    subcategory_id: str,
    user_data: UpdateSubCategory,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Updating subcategory: {subcategory_id}"
    )

    try:

        updated_subcategory = modify_subcategory(
            db=db,
            subcategory_id=subcategory_id,
            data=user_data
        )

        logger.info(
            f"Subcategory updated successfully: {subcategory_id}"
        )

        return updated_subcategory

    except NotFoundException as e:

        logger.warning(
            f"Subcategory not found for update: {subcategory_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# DELETE SUBCATEGORY
@router.delete("/{subcategory_id}")
def delete_subcategory_route(
    subcategory_id: str,
    db: Session = Depends(get_db)
):

    logger.info(
        f"Deleting subcategory: {subcategory_id}"
    )

    try:

        response = remove_subcategory(
            db,
            subcategory_id
        )

        logger.info(
            f"Subcategory deleted successfully: {subcategory_id}"
        )

        return response

    except NotFoundException as e:

        logger.warning(
            f"Subcategory not found for deletion: {subcategory_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )