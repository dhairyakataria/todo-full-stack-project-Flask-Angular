from todo import db

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
       self.password = password  