import contextvars

import falcon
from werkzeug.serving import run_simple

from matando_o_vault.models import Question, QuestionSchema
from matando_o_vault.utils.db import setup_db, SQLOrmDataProvider, SQLMessagePackResource, SQLJsonResource

db_connection = contextvars.ContextVar("db_connection")


def get_app(db_connection_url='sqlite:///db.sqlite3', sql_debug=False):
    app = falcon.API()
    db_session = setup_db(db_connection_url, sql_debug=sql_debug)
    db_connection.set(db_session)

    pedidos_messagepack_resource = SQLMessagePackResource(data_provider=SQLOrmDataProvider(session=db_connection.get(),
                                                                               model=Question,
                                                                               schema=QuestionSchema()))
    pedidos_json_resource = SQLJsonResource(data_provider=SQLOrmDataProvider(session=db_connection.get(),
                                            model=Question,
                                            schema=QuestionSchema()))

    app.add_route('/api/v1/quests', pedidos_json_resource)
    app.add_route('/api/v2/quests', pedidos_messagepack_resource)

    return app


if __name__ == '__main__':
    app = get_app()

    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
