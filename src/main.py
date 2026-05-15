from fastapi import FastAPI

from src.core.config import settings

from src.routes.user_routes import router

from src.db.session_db import engine, Base

from src.models.user_model import User
from src.models.otp_model import OTPVerification
from src.models.token_model import UserToken


app = FastAPI()



app.include_router(router)


@app.get("/info")
def fun():

    return {
        "message": "This is a True Statement"
    }

# print(Base.metadata.tables.keys())





Base.metadata.create_all(bind=engine)