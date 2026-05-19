class InvalidTokenException(Exception):

    def __init__(
        self,
        message="Invalid token"
    ):

        self.message = message

        super().__init__(self.message)


class TokenExpiredException(Exception):

    def __init__(
        self,
        message="Token has expired"
    ):

        self.message = message

        super().__init__(self.message)


class RevokedTokenException(Exception):

    def __init__(
        self,
        message="Token has been revoked"
    ):

        self.message = message

        super().__init__(self.message)