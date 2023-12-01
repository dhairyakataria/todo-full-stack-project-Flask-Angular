from enum import Enum
from marshmallow import Schema, fields


# Schema for user data
class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

# Schema for querying user data
class UserQuerySchema(Schema):
    username = fields.Str(required=True)


# Schema for success messages
class SuccessMessageSchema(Schema):
    message = fields.Str(dump_only=True)