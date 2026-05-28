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

from src.core.logger import logger

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

    logger.info(
        f"Received seller profile creation request: {user_data.user_id}"
    )

    try:

        seller = generate_seller_information(
            db=db,
            data=user_data
        )

        logger.info(
            f"Seller profile created successfully: {seller.id}"
        )

        return seller

    except AlreadyExistsException as e:

        logger.warning(
            f"Seller profile already exists: {user_data.user_id}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except NotFoundException as e:

        logger.warning(
            f"User not found for seller profile: {user_data.user_id}"
        )

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

    logger.info(
        f"Fetching seller profile: {seller_id}"
    )

    try:

        return fetch_seller_information(
            db,
            seller_id
        )

    except NotFoundException as e:

        logger.warning(
            f"Seller profile not found: {seller_id}"
        )

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

    logger.info(
        f"Updating seller profile: {seller_id}"
    )

    try:

        updated_seller = modify_seller_information(
            db=db,
            seller_id=seller_id,
            data=user_data
        )

        logger.info(
            f"Seller profile updated successfully: {seller_id}"
        )

        return updated_seller

    except NotFoundException as e:

        logger.warning(
            f"Seller profile not found for update: {seller_id}"
        )

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )