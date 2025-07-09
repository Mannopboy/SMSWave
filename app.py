from flask import Flask, jsonify, request
from flask_sock import Sock

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.models.models import *

app = Flask(__name__, static_folder="frontend/build", static_url_path="/")
sock = Sock(app)
connections = []
CORS(app)

app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = '/api'

from backend.routes.base_routes import *
from backend.sim.route import *
from backend.api.route import *
from backend.category.route import *
from backend.statistics.route import *

if __name__ == '__main__':
    app.run()
