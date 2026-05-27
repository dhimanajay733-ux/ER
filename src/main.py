from fastapi import FastAPI
from src.core.config import settings
from src.routes.user_routes import router
from src.db.session_db import engine, Base
from src.models.user_model import User
from src.models.otp_model import OTPVerification
from src.models.token_model import UserToken
from src.models.category_model import Category
from src.models.subcategory_model import SubCategory
from src.models.products_model import Product
from src.routes.otp_routes import router as otp_router
from src.routes.forgot_password_routes import(
     router as auth_routers
)
from src.routes.reset_password_sevice import(
    router as auth_router
)
from src.routes.resend_otp_routes import(
     router as resend_routers
)
from src.routes.product_router import router as product_router
from src.routes.category_routes import router as category_router
from src.routes.subcategory_routes import router as sub_category_router
from src.routes.seller_information_routes import router as store_router

app = FastAPI()
app.include_router(router)


@app.get("/info")
def fun():

    return {
        "message": "This is a Production ready Code"
    }

app.include_router(otp_router)
app.include_router(auth_routers)
app.include_router(auth_router)
app.include_router(resend_routers)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(sub_category_router)
app.include_router(store_router)


# print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)