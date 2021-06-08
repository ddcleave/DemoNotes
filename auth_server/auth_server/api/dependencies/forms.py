from fastapi.param_functions import Form
from pydantic.networks import EmailStr


class RegistrationForm:
    def __init__(
        self,
        username: str = Form(..., min_length=3, max_length=50),
        email: EmailStr = Form(...),
        full_name: str = Form(..., min_length=3, max_length=50),
        password: str = Form(..., min_length=8, max_length=50)
    ) -> None:
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password = password


class PasswordRequestForm:
    def __init__(
        self,
        username: str = Form(..., min_length=3, max_length=50),
        password: str = Form(..., min_length=8, max_length=50),
        fingerprint: str = Form(..., min_length=32, max_length=256)
    ):
        self.username = username
        self.password = password
        self.fingerprint = fingerprint
