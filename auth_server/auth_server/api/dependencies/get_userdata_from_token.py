from fastapi.param_functions import Depends
from auth_server.core.config import get_settings
from fastapi import HTTPException, status, Form
from jose import JWTError, jwt
from auth_server.api.dependencies.queries_to_redis import get_userdata


def _get_userdata_from_token(scope: str):
    def inner(token: str = Form(...)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

        try:
            payload = jwt.decode(token, get_settings().secret_key,
                                 algorithms=[get_settings().algorithm])
            if payload.get("scope") != scope:
                raise credentials_exception
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username
    return inner


get_username_from_registration_token = _get_userdata_from_token("registration")

get_username_from_restore_token = _get_userdata_from_token("restore")


def get_userdata_from_registration_token(
    username: str = Depends(get_username_from_registration_token)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    userdata = get_userdata(username)
    if userdata is None:
        raise credentials_exception
    return userdata
