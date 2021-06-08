import sqlalchemy
from pydantic.networks import EmailStr


from .schema import users_table


# def select_confirmed_username_and_email(username: str, email: EmailStr):
#     return users_table.select().where(
#         sqlalchemy.sql.or_(
#             users_table.c.username == username,
#             users_table.c.email == email
#         )
#     )


def get_user_from_db(username: str):
    return users_table.select().where(
        users_table.c.username == username
    )


def insert_new_user(username: str, full_name: str,
                    email: EmailStr, hash_password: str):
    return users_table.insert().values(
        username=username,
        full_name=full_name,
        email=email,
        hashed_password=hash_password
    )


def update_password(username: str, hash_password: str):
    return users_table.update().where(users_table.c.username == username).\
        values(hashed_password=hash_password)
