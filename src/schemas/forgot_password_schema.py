from pydantic import BaseModel, EmailStr


class ForgotPasswordRequest(BaseModel):

    email: EmailStr

class ResetPasswordRequest(BaseModel):

    user_id: str
    otp_code: str
    new_password: str
    confirm_password: str