from main import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class User(UserMixin,db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    rights = db.Column(db.String(1000))
    
    
class Rights(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    rights = db.Column(db.String(1000))