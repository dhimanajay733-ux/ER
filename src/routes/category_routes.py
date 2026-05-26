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

    try:

        return generate_category(
            db=db,
            data=user_data
        )

    except AlreadyExistsException as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# GET ALL CATEGORIES
@router.get("/")
def get_all_categories_route(
    db: Session = Depends(get_db)
):

    return fetch_all_categories(db)


# GET SINGLE CATEGORY
@router.get("/{category_id}")
def get_single_category_route(
    category_id: str,
    db: Session = Depends(get_db)
):

    try:

        return fetch_single_category(
            db,
            category_id
        )

    except NotFoundException as e:

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

    try:

        return modify_category(
            db=db,
            category_id=category_id,
            data=user_data
        )

    except NotFoundException as e:

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

    try:

        return remove_category(
            db,
            category_id
        )

    except NotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )