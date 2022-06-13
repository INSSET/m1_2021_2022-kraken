from flask import Flask, Response
from flask.cli import load_dotenv
from flask_cors import CORS

from router.groups_routes import groups_routes
from router.users_routes import users_routes

app = Flask(__name__)
app.register_blueprint(users_routes)
app.register_blueprint(groups_routes)

app.config["DEBUG"] = True
CORS(app)
load_dotenv()


@app.route('/', methods=['GET'])
def home():
    return Response('Hello Python', mimetype='application/json', status=200)


@app.route('/api/', methods=['GET'])
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def private():
    return Response('Bonjour Harold', mimetype='application/json', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
