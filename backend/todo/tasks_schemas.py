from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=False)
    task_description = fields.String(required=True, validate=validate.Length(max=255))
    # due_date = fields.DateTime(allow_none=True)
    completed = fields.Boolean(default=False)

class TaskUpdateSchema(Schema):
    task_id = fields.Integer(required=True)
    user_id = fields.Integer()
    task_description = fields.String(required=True, validate=validate.Length(max=255))
    completed = fields.Boolean(default=False)

class TaskQuerySchema(Schema):
    task_id = fields.Integer()

class SuccessMessageSchema(Schema):
    message = fields.String()