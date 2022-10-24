from api.user.application.password_hash import get_password_hash
from api.user.application.password_hash import verify_password


def test_verify_password_true() -> None:
    plain_password = "test"
    hashed_password = get_password_hash(password=plain_password)
    assert verify_password(plain_password=plain_password, hashed_password=hashed_password) is True


def test_verify_password_false() -> None:
    plain_password = "test"
    hashed_password = get_password_hash(password=plain_password)
    assert verify_password(plain_password=f"no{plain_password}", hashed_password=hashed_password) is False
