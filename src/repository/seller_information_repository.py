from sqlalchemy.orm import Session

from src.models.seller_information_model import (
    SellerInformation
)

from src.schemas.seller_information_schema import (
    CreateSellerInformation,
    UpdateSellerInformation
)

from src.core.logger import logger

from src.exceptions.database_exception import (
    DatabaseInsertException,
    DatabaseFetchException,
    DatabaseUpdateException
)


# CREATE SELLER INFO
def create_seller_information(
    db: Session,
    data: CreateSellerInformation
):

    try:

        new_seller = SellerInformation(

            user_id=data.user_id,

            store_name=data.store_name
        )

        db.add(new_seller)

        db.flush()

        db.refresh(new_seller)

        return new_seller

    except Exception as e:

        logger.error(
            f"Failed to create seller profile: {str(e)}"
        )

        raise DatabaseInsertException()


# GET BY USER ID
def get_seller_by_user_id(
    db: Session,
    user_id: str
):

    try:

        query = (
            db.query(SellerInformation)
            .filter(SellerInformation.user_id == user_id)
        )

        seller = query.first()

        return seller

    except Exception as e:

        logger.error(
            f"Failed to fetch seller by user id: {str(e)}"
        )

        raise DatabaseFetchException()


# GET BY ID
def get_seller_by_id(
    db: Session,
    seller_id: int
):

    try:

        query = (
            db.query(SellerInformation)
            .filter(SellerInformation.id == seller_id)
        )

        seller = query.first()

        return seller

    except Exception as e:

        logger.error(
            f"Failed to fetch seller by id: {str(e)}"
        )

        raise DatabaseFetchException()


# UPDATE
def update_seller_information(
    db: Session,
    seller: SellerInformation,
    data: UpdateSellerInformation
):

    try:

        if data.store_name is not None:

            seller.store_name = data.store_name

        if data.status is not None:

            seller.status = data.status

        db.add(seller)

        db.flush()

        db.refresh(seller)

        return seller

    except Exception as e:

        logger.error(
            f"Failed to update seller profile: {str(e)}"
        )

        raise DatabaseUpdateException()