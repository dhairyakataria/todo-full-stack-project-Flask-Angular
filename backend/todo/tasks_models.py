from sqlalchemy import ForeignKey
from todo import db

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    print("creating task")
    id = db.Column('task_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    # due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, task_description, completed=False):
        self.user_id = user_id
        self.task_description = task_description
        self.completed = completed