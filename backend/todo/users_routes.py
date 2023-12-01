from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from todo import db
from todo.users_schemas import UserQuerySchema, UserSchema, SuccessMessageSchema
from todo.users_models import UsersModel
import hashlib

# Create a Flask Blueprint for user operations
blp = Blueprint("users", __name__, description="Operations for users")

@blp.route("/user")
class Users(MethodView):
    def __init__(self) -> None:
        self.db = db
    
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
            password = hashlib.sha256(user_data["password"].encode('utf-8')).hexdigest()

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