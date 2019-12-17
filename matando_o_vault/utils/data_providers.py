from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.orm import Session

from utils.db import Base


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
