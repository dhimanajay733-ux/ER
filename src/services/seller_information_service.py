from sqlalchemy.orm import Session

from src.schemas.seller_information_schema import (
    CreateSellerInformation,
    UpdateSellerInformation
)

from src.repository.seller_information_repository import (
    create_seller_information,
    get_seller_by_user_id,
    get_seller_by_id,
    update_seller_information
)

from src.repository.user_repository import (
    get_user_by_id
)

from src.exceptions.common_exception import (
    AlreadyExistsException,
    NotFoundException
)

from src.core.logger import logger


# CREATE SELLER INFO
def generate_seller_information(
    db: Session,
    data: CreateSellerInformation
):

    logger.info(
        f"Checking user existence: {data.user_id}"
    )

    # CHECK USER EXISTS
    user = get_user_by_id(
        db,
        data.user_id
    )

    if not user:

        logger.warning(
            f"User not found: {data.user_id}"
        )

        raise NotFoundException(
            "User not found"
        )

    logger.info(
        f"Checking existing seller profile: {data.user_id}"
    )

    # CHECK ALREADY EXISTS
    existing_seller = get_seller_by_user_id(
        db,
        data.user_id
    )

    if existing_seller:

        logger.warning(
            f"Seller profile already exists: {data.user_id}"
        )

        raise AlreadyExistsException(
            "Seller profile already exists"
        )

    try:

        logger.info(
            f"Creating seller profile: {data.user_id}"
        )

        new_seller = create_seller_information(
            db=db,
            data=data
        )

        db.commit()

        logger.info(
            f"Seller profile committed successfully: {new_seller.id}"
        )

        return new_seller

    except Exception as e:

        db.rollback()

        logger.error(
            f"Seller profile creation failed: {str(e)}"
        )

        raise e


# GET SELLER INFO
def fetch_seller_information(
    db: Session,
    seller_id: int
):

    logger.info(
        f"Fetching seller profile by id: {seller_id}"
    )

    seller = get_seller_by_id(
        db,
        seller_id
    )

    if not seller:

        logger.warning(
            f"Seller profile not found: {seller_id}"
        )

        raise NotFoundException(
            "Seller profile not found"
        )

    return seller


# UPDATE SELLER INFO
def modify_seller_information(
    db: Session,
    seller_id: int,
    data: UpdateSellerInformation
):

    logger.info(
        f"Checking seller profile before update: {seller_id}"
    )

    seller = get_seller_by_id(
        db,
        seller_id
    )

    if not seller:

        logger.warning(
            f"Seller profile not found for update: {seller_id}"
        )

        raise NotFoundException(
            "Seller profile not found"
        )

    try:

        logger.info(
            f"Updating seller profile: {seller_id}"
        )

        updated_seller = update_seller_information(
            db=db,
            seller=seller,
            data=data
        )

        db.commit()

        logger.info(
            f"Seller profile updated successfully: {seller_id}"
        )

        return updated_seller

    except Exception as e:

        db.rollback()

        logger.error(
            f"Seller profile update failed: {str(e)}"
        )

        raise e