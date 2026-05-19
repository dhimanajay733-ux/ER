class UserAlreadyExistsException(Exception):

    def __init__(
        self,
        message="User with this email already exists"
    ):

        self.message = message

        super().__init__(self.message)


class InvalidCredentialsException(Exception):

    def __init__(
        self,
        message="Invalid email or password"
    ):

        self.message = message

        super().__init__(self.message)


class UserNotFoundException(Exception):

    def __init__(
        self,
        message="User not found"
    ):

        self.message = message

        super().__init__(self.message)


class UserNotVerifiedException(Exception):

    def __init__(
        self,
        message="User is not verified"
    ):

        self.message = message

        super().__init__(self.message)