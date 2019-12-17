import json

import falcon

import msgpack


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
