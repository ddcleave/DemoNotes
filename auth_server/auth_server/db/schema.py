from sqlalchemy import (
    MetaData, Table, Column, Integer, String
)


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',

    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

users_table = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('username', String, nullable=False, index=True),
    Column('full_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False)
)
