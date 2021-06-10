from auth_server.models.models import User
from auth_server.db.schema import users_table
from sqlalchemy.sql import or_
from auth_server.db.database import database
from auth_server.db.queries import insert_new_user, update_password


async def exist_confirmed_username_or_email_in_db(username: str,
                                                  email: str) -> bool:
    query = users_table.select().where(
        or_(
            users_table.c.username == username,
            users_table.c.email == email
        )
    )
    result = await database.fetch_one(query)
    if result:
        return True
    return False


async def exist_username_in_db(username: str) -> bool:
    query = users_table.select().where(
        users_table.c.username == username
    )
    result = await database.fetch_one(query)
    if result:
        return True
    return False


async def exist_email_in_db(email: str) -> bool:
    query = users_table.select().where(
        users_table.c.email == email
    )
    result = await database.fetch_one(query)
    if result:
        return True
    return False


async def create_new_user(username: str, full_name: str,
                          email: str, hash_password: str):
    await database.execute(insert_new_user(username, full_name,
                                           email, hash_password))


async def replace_password(username: str, hash_password: str):
    await database.execute(update_password(username, hash_password))


async def get_userdata_from_email(email: str):
    query = users_table.select().where(
        users_table.c.email == email
    )
    result = await database.fetch_one(query)
    return User(**result)
