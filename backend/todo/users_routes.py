from flask import abort, current_app
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity, create_refresh_token

from todo import jwt
from todo import db, app
from todo.users_schemas import UserQuerySchema, UserSchema, SuccessMessageSchema, LoginResponseSchema
from todo.users_models import UsersModel
# from todo.blocklist import BLOCKLIST

# Create a Flask Blueprint for user operations
blp = Blueprint("users", __name__, description="Operations for users")


@blp.app_context_processor
def inject_jwt():
    return dict(jwt=jwt)

@blp.route("/login", methods=["POST"])
class Login(MethodView):
    @blp.response(200, LoginResponseSchema)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            username = user_data["username"]
            password = user_data["password"]

            user = UsersModel.authenticate(username, password)

            if user:
                # Create JWT access token
                access_token = create_access_token(identity=user.id)
                
                # Create JWT refresh token
                # refresh_token = create_refresh_token(identity=user.id)
                print(access_token)
                return {'message': 'Login successful', 'access_token': access_token}, 200
            else:
                return {'message': 'Invalid credentials'}, 401

        except Exception as e:
            current_app.logger.error(f"Error during login: {str(e)}")
            abort(500, description=f"Internal Server Error: {str(e)}")


@blp.route("/logout", methods=["POST"])
class Logout(MethodView):
    @blp.response(200, SuccessMessageSchema)
    @jwt_required()
    def post(self):
        try:
            # Get the unique identifier of the current token
            jti = get_jwt()['jti']

            # Add the token identifier to the blacklist
            current_app.config['BLACKLIST'].add(jti)
            # Access token is automatically invalidated upon logout
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            current_app.logger.error(f"Error during logout: {str(e)}")
            abort(500, description=f"Internal Server Error: {str(e)}")


@blp.route("/user")
class Users(MethodView):
    def __init__(self) -> None:
        self.db = db

    @jwt_required()
    @blp.response(201, UserSchema(many=True))
    def get(self):
        try:
            list_user = []
            users = UsersModel.query.all()
            sch = UserSchema()
            for user in users:
                # print("-------",sch.dump(user))
                # print(user.__dict__)
                list_user.append(sch.dump(user))
            return list_user
        except Exception as e:
            abort(500, message=f"Internal Server Error: {str(e)}")


    @blp.response(201, SuccessMessageSchema)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            username = user_data["username"]
            email = user_data["email"]
            password = user_data['password']

            existing_user = UsersModel.query.filter_by(username=username).first()

            if existing_user:
                return {"message": "User already exits"}, 403

            new_user = UsersModel(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return {"message": "User added successfully"}, 201

        except Exception as e:
            # Log the exception for further analysis
            print(f"Error: {str(e)}")

            # Depending on your needs, you might want to return a more specific error response
            abort(500, description="Internal Server Error")
    
        finally:
            # Always close the session in a finally block to ensure proper cleanup
            db.session.close()
    

    """Delete a user by ID."""
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def delete(self, args):
        try:
            username = args.get('username')
            print(username)
            user = UsersModel.query.filter_by(username=username).first()

            if user:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted successfully'}
            else:
                print("hiiiiiiiii")
                return {'message': 'User not found'}, 404
        except Exception as e:
            abort(500, description=f"Internal Server Error: {str(e)}")

class UserNotFoundException(Exception):
    pass

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    return jti in app.config['BLACKLIST']