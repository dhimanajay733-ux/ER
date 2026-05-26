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

    try:

        return generate_subcategory(
            db=db,
            data=user_data
        )

    except AlreadyExistsException as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except NotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# GET ALL SUBCATEGORIES
@router.get("/")
def get_all_subcategories_route(
    db: Session = Depends(get_db)
):

    return fetch_all_subcategories(db)


# GET SINGLE SUBCATEGORY
@router.get("/{subcategory_id}")
def get_single_subcategory_route(
    subcategory_id: str,
    db: Session = Depends(get_db)
):

    try:

        return fetch_single_subcategory(
            db,
            subcategory_id
        )

    except NotFoundException as e:

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

    try:

        return modify_subcategory(
            db=db,
            subcategory_id=subcategory_id,
            data=user_data
        )

    except NotFoundException as e:

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

    try:

        return remove_subcategory(
            db,
            subcategory_id
        )

    except NotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )