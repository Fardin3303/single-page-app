import logging
from alembic import command
from pathlib import Path
from alembic.config import Config as AlembicConfig
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine


LOGGER = logging.getLogger(__name__)


def check_and_migrate_database():
    try:
        alembic_ini_path = Path(__file__).parent.parent.joinpath("alembic.ini")
        LOGGER.info(f"alembic_ini_path: {alembic_ini_path}")
        alembic_cfg = AlembicConfig(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", str(Path(alembic_ini_path).parent.joinpath("alembic_migrations")))
        LOGGER.info(f"script_location: {alembic_cfg.get_main_option('script_location')}")
        database_url =alembic_cfg.get_main_option("sqlalchemy.url")
        engine = create_engine(database_url)
        # Get current revision from database
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_revision_from_db = context.get_current_revision()
            LOGGER.info(f"Current revision from database: {current_revision_from_db}")
        
        # Get head revision from alembic config
        script = ScriptDirectory.from_config(alembic_cfg)
        head_revision = script.get_current_head()
        LOGGER.info(f"Head alembic revision from config: {head_revision}")

        # If the database is not up to date, migrate
        if current_revision_from_db != head_revision:
            LOGGER.info("Database is not up to date, migrating...")
            command.upgrade(alembic_cfg, "head")
            LOGGER.info("Database migrated to the latest revision.")
        else:
            LOGGER.info("Database is up to date.")
    except Exception as e:
        LOGGER.exception(f"Error while checking and migrating database: {e}")

if __name__ == "__main__":
    check_and_migrate_database()