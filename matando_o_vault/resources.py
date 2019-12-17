

class StaticSecretResource:
    def __init__(self, credentials):
        self.credentials = credentials

    def on_get(self, req, resp):
        resp.body = self.credentials
