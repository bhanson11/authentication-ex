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
        return cls(username=username, password=hashed_pw, first_name=first_name, last_name=last_name, email=email)
    
    @classmethod
    def authenticate(cls, username, password):
        """authenticate user with username and pw"""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False
    
"""models for feedback"""
class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)

    user = db.relationship('User', backref=db.backref('feedback', cascade='all, delete-orphan'))

