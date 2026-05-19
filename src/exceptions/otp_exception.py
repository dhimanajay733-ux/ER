class OTPGenerationException(Exception):

    def __init__(
        self,
        message="Failed to generate OTP"
    ):

        self.message = message

        super().__init__(self.message)


class OTPExpiredException(Exception):

    def __init__(
        self,
        message="OTP has expired"
    ):

        self.message = message

        super().__init__(self.message)


class OTPInvalidException(Exception):

    def __init__(
        self,
        message="Invalid OTP"
    ):

        self.message = message

        super().__init__(self.message)


class EmailSendingException(Exception):

    def __init__(
        self,
        message="Failed to send email"
    ):

        self.message = message

        super().__init__(self.message)