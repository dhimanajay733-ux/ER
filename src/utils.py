import random, uuid


def generate_uuid() -> str:

    return str(uuid.uuid4())


# GENERATE OTP
def create_otp():

    # random.randint(100000, 999999)
    # generates a random 6-digit number.

    # str(...)
    # converts the number into string format
    # so it can be sent easily in emails/SMS.

    return str(
        random.randint(100000, 999999)
    )