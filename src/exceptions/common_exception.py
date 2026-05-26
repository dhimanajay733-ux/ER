class AlreadyExistsException(Exception):

    def __init__(
        self,
        message="Resource already exists"
    ):

        self.message = message

        super().__init__(self.message)


class NotFoundException(Exception):

    def __init__(
        self,
        message="Resource not found"
    ):

        self.message = message

        super().__init__(self.message)