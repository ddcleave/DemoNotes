from fastapi.param_functions import Body, Depends
from auth_server.core.config import get_settings
from fastapi import HTTPException, status
from jose import JWTError, jwt
from auth_server.api.dependencies.queries_to_redis import get_userdata


def _get_subject_from_token(scope: str):
    def inner(token: str = Body(..., embed=True)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

        try:
            payload = jwt.decode(token, get_settings().secret_key,
                                 algorithms=[get_settings().algorithm])
            if payload.get("scope") != scope:
                raise credentials_exception
            subject = payload.get("sub")
            if subject is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return subject
    return inner


get_username_from_registration_token = _get_subject_from_token("registration")

get_email_from_restore_token = _get_subject_from_token("restore")


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
