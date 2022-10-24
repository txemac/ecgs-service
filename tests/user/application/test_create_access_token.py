from api.user.application.create_access_token import create_access_token


def test_create_access_token() -> None:
    token = create_access_token(email="txema.bermudez@gmail.com")
    assert token.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.")
