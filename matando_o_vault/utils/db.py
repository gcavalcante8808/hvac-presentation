import falcon
import json
import msgpack
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
Base = declarative_base()


def setup_db(db_connection_url, sql_debug=False):
    engine = create_engine(
        db_connection_url,
        echo=sql_debug
    )

    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)

    return scoped_session(session_factory)


class SQLOrmDataProvider:
    def __init__(self, session: Session, model: Base, schema: ModelSchema):
        self.session = session
        self.model = model
        self.schema = schema

    def get(self, ids=None):
        if not ids:
            queryset = self.session.query(self.model).all()
            return self.schema.dump(queryset, many=True)

        queryset = self.session.query(self.model).filter(self.model.id.in_(ids))
        return self.schema.dump(queryset, many=True)


class SQLMessagePackResource:
    def __init__(self, data_provider):
        self.data_provider = data_provider

    def on_get(self, req, resp):
        resp.data = msgpack.packb(self.data_provider.get(), use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200


class SQLJsonResource:
    def __init__(self, data_provider):
        self.data_provider = data_provider

    def on_get(self, req, resp):
        resp.data = json.dumps(self.data_provider.get()).encode()
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
