from flask import abort
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from todo.tasks_schemas import TaskQuerySchema, TaskSchema, SuccessMessageSchema, TaskUpdateSchema
from todo import db
from todo.tasks_models import TaskModel

# Create a Flask Blueprint for tasks operations
blp = Blueprint("tasks", __name__, description="Operations for tasks")


@blp.route("/tasks")
class Tasks(MethodView):
    def __init__(self) -> None:
        self.db = db
    
    @blp.response(200, TaskSchema(many=True))
    @jwt_required()  # Require a valid JWT token for this route
    def get(self):
        try:
            list_tasks = []
            # Extract user_id from the JWT token
            user_id = get_jwt_identity()
            print("user id  ", user_id)
            # Use the user_id to fetch tasks specific to that user
            tasks = TaskModel.query.filter_by(user_id=user_id).all()
            sch = TaskSchema()
            
            # Use many=True to include task_id in the output
            list_tasks = [sch.dump(task) for task in tasks]
        
            return list_tasks
        except Exception as e:
            abort(500, description=f"Internal Server Error: {str(e)}")

    @blp.response(201, SuccessMessageSchema)
    @blp.arguments(TaskSchema)
    @jwt_required()  # Require a valid JWT token for this route
    def post(self, task_data):
        try:
            user_id = get_jwt_identity()
            print(user_id)
            task_description = task_data["task_description"]
            # due_date = task_data.get("due_date")
            completed = task_data.get("completed", False)

            new_task = TaskModel(user_id=user_id, task_description=task_description, completed=completed)
            db.session.add(new_task)
            db.session.commit()

            return {"message": "Task added successfully"}, 201

        except Exception as e:
            print(f"Error: {str(e)}")
            abort(500, description="Internal Server Error")
    
        finally:
            db.session.close()

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(TaskQuerySchema, location="query")
    def delete(self, args):
        try:
            task_id = args.get('task_id')
            task = TaskModel.query.get(task_id)

            if task:
                db.session.delete(task)
                db.session.commit()
                return {'message': 'Task deleted successfully'}
            else:
                return {'message': 'Task not found'}, 404
        except Exception as e:
            abort(500, description=f"Internal Server Error: {str(e)}")

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(TaskUpdateSchema)
    def put(self, task_data):
        try:
            task_id = task_data["task_id"]
            task = TaskModel.query.get(task_id)
            print(task_data)
            if task:
                # Update task fields based on the provided data
                task.user_id = task_data.get("user_id", task.user_id)
                task.task_description = task_data.get("task_description", task.task_description)
                task.completed = task_data.get("completed", task.completed)

                db.session.commit()
                return {'message': 'Task updated successfully'}
            else:
                return {'message': 'Task not found'}, 404

        except Exception as e:
            abort(500, description=f"Internal Server Error: {str(e)}")