class DatabaseInsertException(Exception):

    def __init__(
        self,
        message="Failed to insert data into database"
    ):

        self.message = message

        super().__init__(self.message)


class DatabaseFetchException(Exception):

    def __init__(
        self,
        message="Failed to fetch data from database"
    ):

        self.message = message

        super().__init__(self.message)


class DatabaseUpdateException(Exception):

    def __init__(
        self,
        message="Failed to update database"
    ):

        self.message = message

        super().__init__(self.message)