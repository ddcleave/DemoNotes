import os
from pathlib import Path

from alembic.config import Config

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()


def make_alembic_config(config_file: str, ini_section: str, pg_url: str,
                        base_path: str = PROJECT_PATH) -> Config:
    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(config_file):
        config_file = os.path.join(base_path, config_file)

    config = Config(file_=config_file, ini_section=ini_section)

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    config.set_main_option('sqlalchemy.url', pg_url)

    return config