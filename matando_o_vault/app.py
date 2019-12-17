import contextvars
import json

import falcon
from werkzeug.serving import run_simple

from models.question import Question, QuestionSchema
from utils.base_resources import SQLMessagePackResource, SQLJsonResource
from utils.credential import get_vault_client, get_static_credentials
from utils.data_providers import SQLOrmDataProvider
from utils.db import setup_db_connection, db_connection


vault_client = contextvars.ContextVar('vault_client')


def get_app(sql_debug=False):
    vault_client.set(get_vault_client())
    setup_db_connection(sql_debug, vault_client.get())

    app = falcon.API()
    setup_routes(app)

    return app


def setup_routes(app: falcon.API):
    pedidos_messagepack_resource = SQLMessagePackResource(data_provider=SQLOrmDataProvider(session=db_connection.get(),
                                                                                           model=Question,
                                                                                           schema=QuestionSchema()))
    pedidos_json_resource = SQLJsonResource(data_provider=SQLOrmDataProvider(session=db_connection.get(),
                                                                             model=Question,
                                                                             schema=QuestionSchema()))

    static_credentials_resource = StaticCredentialResource(vault_client.get())

    app.add_route('/static_secrets', static_credentials_resource)
    app.add_route('/api/v1/question', pedidos_json_resource)
    app.add_route('/api/v2/question', pedidos_messagepack_resource)


class StaticCredentialResource:
    def __init__(self, vault_client):
        self.vault_client = vault_client

    def on_get(self, req, resp):
        resp.data = json.dumps(get_static_credentials(vault_client=self.vault_client)).encode()



if __name__ == '__main__':
    app = get_app()

    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
