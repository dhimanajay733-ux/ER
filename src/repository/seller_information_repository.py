from sqlalchemy.orm import Session

from src.models.seller_information_model import (
    SellerInformation
)

from src.schemas.seller_information_schema import (
    CreateSellerInformation,
    UpdateSellerInformation
)


# CREATE SELLER INFO
def create_seller_information(
    db: Session,
    data: CreateSellerInformation
):

    new_seller = SellerInformation(

        user_id=data.user_id,

        store_name=data.store_name
    )

    db.add(new_seller)

    db.flush()

    db.refresh(new_seller)

    return new_seller


# GET BY USER ID
def get_seller_by_user_id(
    db: Session,
    user_id: str
):

    return (
        db.query(SellerInformation)
        .filter(SellerInformation.user_id == user_id)
        .first()
    )


# GET BY ID
def get_seller_by_id(
    db: Session,
    seller_id: int
):

    return (
        db.query(SellerInformation)
        .filter(SellerInformation.id == seller_id)
        .first()
    )


# UPDATE
def update_seller_information(
    db: Session,
    seller: SellerInformation,
    data: UpdateSellerInformation
):

    if data.store_name is not None:

        seller.store_name = data.store_name

    if data.status is not None:

        seller.status = data.status

    db.add(seller)

    db.flush()

    db.refresh(seller)

    return seller