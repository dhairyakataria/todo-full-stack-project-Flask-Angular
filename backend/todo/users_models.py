from todo import db
import hashlib

class UsersModel(db.Model):  
    __tablename__ = 'users'

    print("creating user")
    id = db.Column('user_id', db.Integer, primary_key = True)  
    username = db.Column(db.String(50), unique=True, nullable=False)  
    email = db.Column(db.String(50))  
    password = db.Column(db.String(64), nullable=False) 

    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()  

    @staticmethod
    def authenticate(username, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = UsersModel.query.filter_by(username=username, password=hashed_password).first()
        return user