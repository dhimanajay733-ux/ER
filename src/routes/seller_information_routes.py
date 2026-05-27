from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from src.db.session_db import get_db

from src.schemas.seller_information_schema import (
    CreateSellerInformation,
    UpdateSellerInformation
)

from src.services.seller_information_service import (
    generate_seller_information,
    fetch_seller_information,
    modify_seller_information
)

from src.exceptions.common_exception import (
    AlreadyExistsException,
    NotFoundException
)

router = APIRouter(
    prefix="/api/seller-information",
    tags=["Seller Information"]
)


# CREATE
@router.post("/")
def create_seller_information_route(
    user_data: CreateSellerInformation,
    db: Session = Depends(get_db)
):

    try:

        return generate_seller_information(
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


# GET
@router.get("/{seller_id}")
def get_seller_information_route(
    seller_id: int,
    db: Session = Depends(get_db)
):

    try:

        return fetch_seller_information(
            db,
            seller_id
        )

    except NotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# UPDATE
@router.put("/{seller_id}")
def update_seller_information_route(
    seller_id: int,
    user_data: UpdateSellerInformation,
    db: Session = Depends(get_db)
):

    try:

        return modify_seller_information(
            db=db,
            seller_id=seller_id,
            data=user_data
        )

    except NotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )