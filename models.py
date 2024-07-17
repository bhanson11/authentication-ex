from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

"""models for app"""
class User(db.Model):
    __tablename__ = 'users' # Add table name

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """register new user with hashed password and return user"""
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        return cls(username=username, password=hashed_pw, first_name=first_name, last_name=last_name)
    
    