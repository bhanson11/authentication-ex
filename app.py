from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authentication"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretauth"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
# db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['GET'])
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    

@app.route('/login', methods=['GET', 'POST'])
def login():


@app.route('/secret', methods=['GET'])
def secret():
