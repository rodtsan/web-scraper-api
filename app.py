from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from gql_schema import schema
from data import session, Base, engine
from api import bp

app = Flask(__name__)
CORS(app, static_folder="/files/temp", resources={r"/*": {"origin": "*"}})

app.add_url_rule(
    rule="/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=True  # for having the GraphiQL interface
    ),
    strict_slashes=False,
)

Base.metadata.create_all(engine)

app.register_blueprint(bp)

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
    
if __name__ == "__main__":
    app.run()