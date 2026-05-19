from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, Field


class VerifyOTPRequest(BaseModel):

    user_id : str
    otp_code: str