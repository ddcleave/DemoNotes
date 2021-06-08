from auth_server.db.database import database
from auth_server.db.schema import users_table
from auth_server.models import UserInDB
from auth_server.services.password import verify_password

from .oauth2 import OAuth2PasswordBearerWithCookie, OAuth2RefreshToken

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")
oauth2_refresh_scheme = OAuth2RefreshToken(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    query = users_table.select().where(
        users_table.c.username == username
    )
    result = await database.fetch_one(query)
    if not result:
        return False
    if not verify_password(password, result['hashed_password']):
        return False
    return UserInDB(**result)
