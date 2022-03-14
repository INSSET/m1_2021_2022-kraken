from flask import Flask, Response
from flask.cli import load_dotenv
from flask_cors import CORS

from router.groups_routes import groups_routes
from router.keys_routes import keys_routes
from router.upload_routes import upload_routes
from router.users_routes import users_routes

app = Flask(__name__)
app.register_blueprint(users_routes)
app.register_blueprint(groups_routes)
app.register_blueprint(upload_routes)
app.register_blueprint(keys_routes)

app.config["DEBUG"] = True
CORS(app)
load_dotenv()


# @app.errorhandler(AuthError)
# def handle_auth_error(ex):
#     response = jsonify(ex.error)
#     response.status_code = ex.status_code
#     return response


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
