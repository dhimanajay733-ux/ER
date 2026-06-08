from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.category_model import Category
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.category_schema import (
    CreateCategory,
    UpdateCategory
)

# CREATE CATEGORY
async def create_category(
    db: AsyncSession,
    data: CreateCategory
):

    new_category =  Category(

        type=data.type,

        description=data.description
    )
    print(type(db))
    db.add(new_category)

    await db.flush()
    await db.refresh(new_category)

    return new_category

# GET CATEGORY BY ID
async def get_category_by_id(
    db: AsyncSession,
    category_id: str
):
    stmt = select(Category).where(Category.id==category_id)

    result = await db.execute(stmt)
     
    category = result.scalars().all()

    return category


# GET CATEGORY BY TYPE
# def get_category_by_type(
#     db: Session,
#     type: str
# ):

#     query = (
#         db.query(Category)
#         .filter(Category.type == type)
#     )

#     category = query.first()

#     return category

async def get_category_by_type(
        db: AsyncSession,
        type: str
):
    stmt=select(Category).where(Category.type == type)

    result= await db.execute(stmt)

    category = result.scalar_one_or_none()

    return  category

# GET ALL CATEGORIES
async def get_all_categories(
    db: AsyncSession
):

# 1. Create a select statement
    statement = select(Category)

    # 2. Await the execution of the statement
    result = await db.execute(statement)

    # 3. Extract the actual database rows/objects
    categories = result.scalars().all()
    print(type(categories))
    return  categories


# UPDATE CATEGORY
async def update_category(
    db: AsyncSession,
    category: Category,
    data: UpdateCategory
):
    for c in category:

        if data.type is not None:

            c.type = data.type
        if data.description is not None:

            c.description = data.description

    # db.add(category)

    # db.flush()

    db.refresh(category)

    return  category


# DELETE CATEGORY
def delete_category(
    db: Session,
    category: Category
):

    db.delete(category)

    db.flush()

    return True