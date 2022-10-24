from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
        plain_password: str,
        hashed_password: str,
) -> bool:
    """
    Check a password.

    :param plain_password: plain password
    :param hashed_password: hashed password
    :return: True if the password is OK
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(
        password: str,
) -> str:
    """
    Generate a hashed password.

    :param password: password
    :return: hashed password
    """
    return PWD_CONTEXT.hash(password)
