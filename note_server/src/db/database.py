from src.core.config import get_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


database = get_settings().database_url

engine = create_engine(database)

Session = sessionmaker(engine)

