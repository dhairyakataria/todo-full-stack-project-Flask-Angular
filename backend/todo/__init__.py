from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Create a Flask app
app = Flask(__name__)

# Configuration for Flask-Smorest and Flask-JWT-Extended
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "To Do list"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.sqlite'  
app.config['SECRET_KEY'] = "d8deb755-84fb-40cb-be01-760f8e62a978"  


# Configure token blacklisting
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# Set up a set to store revoked (blacklisted) tokens
app.config['BLACKLIST'] = set()

jwt = JWTManager(app)

api = Api(app)
db = SQLAlchemy(app)

from todo import users_routes
# Register the User Blueprint
api.register_blueprint(users_routes.blp)
