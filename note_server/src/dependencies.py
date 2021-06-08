from src.core.config import get_settings
from src.services.usecases import BaseUseCase
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException
from src.utils.oauth2_cookies import OAuth2PasswordBearerWithCookie


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def get_user(access_token: str = Depends(oauth2_scheme)):
    # переделать ошибку
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(access_token, get_settings().secret_key,
                             algorithms=[get_settings().algorithm])
        if payload.get("scope") != "user":
            raise credentials_exception
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


