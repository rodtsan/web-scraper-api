from flask import Flask, Response


class EndpointAction(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        response = self.action()
        if response != None:
            return response
        else:
            return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run("0.0.0.0", 5000, debug=True)

    def add_endpoint(
        self, endpoint=None, endpoint_name=None, handler=None, methods=None
    ):
        self.app.add_url_rule(
            endpoint, endpoint_name, EndpointAction(handler), methods=methods
        )

