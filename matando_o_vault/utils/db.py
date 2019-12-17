import contextvars

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from utils.credential import get_database_credentials, get_required_env_var

Base = declarative_base()

db_connection = contextvars.ContextVar("db_connection")


def create_db_sessions(db_connection_url, sql_debug=False):
    engine = create_engine(
        db_connection_url,
        echo=sql_debug
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)

    return scoped_session(session_factory)


def setup_db_connection(sql_debug, vault_client):
    db_host = get_required_env_var('DB_HOST')
    db_name = get_required_env_var('DB_NAME')
    db_user, db_password = get_database_credentials(vault_client)

    db_connection_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
    db_session = create_db_sessions(db_connection_url, sql_debug=sql_debug)
    db_connection.set(db_session)
