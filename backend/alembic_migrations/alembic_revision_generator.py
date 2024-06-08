import sys
import os
from pathlib import Path
import alembic.util.exc
from alembic import command
from alembic.config import Config as AlembicConfig

def generate_autogenerated_revision(revision_message: str, database_url:str):
    print(f"Generating revision for {database_url.split('/')[-1]} database")
    alembic_ini_path = Path(__file__).parent.parent.joinpath("alembic.ini")
    alembic_cfg = AlembicConfig(alembic_ini_path)
    # alembic_cfg.set_main_option("script_location", str(Path(alembic_ini_path).parent))
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    print(f" alembic_cfg: {alembic_cfg}")
    try:
        command.revision(alembic_cfg, message=revision_message,
        head='head', 
        splice=False, 
        autogenerate=True)
    except alembic.util.exc.CommandError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"Revision generated successfully for {database_url.split('/')[-1]} database")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python alembic_revision_generator.py <revision_message> <database_name>" 
        "<database_url>"
        "Example: python alembic_revision_generator.py 'Add new table' 'mydatabase' 'postgresql://postgres:postgres@localhost:5432/mydatabase'"
        )
        sys.exit(1)
    revision_message = sys.argv[1]
    database_url = sys.argv[2]

    generate_autogenerated_revision(revision_message, database_url)