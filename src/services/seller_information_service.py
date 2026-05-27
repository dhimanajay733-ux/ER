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


# CREATE SELLER INFO
def generate_seller_information(
    db: Session,
    data: CreateSellerInformation
):

    # CHECK USER EXISTS
    user = get_user_by_id(
        db,
        data.user_id
    )

    if not user:

        raise NotFoundException(
            "User not found"
        )

    # CHECK ALREADY EXISTS
    existing_seller = get_seller_by_user_id(
        db,
        data.user_id
    )

    if existing_seller:

        raise AlreadyExistsException(
            "Seller profile already exists"
        )

    try:

        new_seller = create_seller_information(
            db=db,
            data=data
        )

        db.commit()

        return new_seller

    except Exception as e:

        db.rollback()

        raise e


# GET SELLER INFO
def fetch_seller_information(
    db: Session,
    seller_id: int
):

    seller = get_seller_by_id(
        db,
        seller_id
    )

    if not seller:

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

    seller = get_seller_by_id(
        db,
        seller_id
    )

    if not seller:

        raise NotFoundException(
            "Seller profile not found"
        )

    try:

        updated_seller = update_seller_information(
            db=db,
            seller=seller,
            data=data
        )

        db.commit()

        return updated_seller

    except Exception as e:

        db.rollback()

        raise e