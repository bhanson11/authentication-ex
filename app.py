from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, bcrypt
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authentication"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretauth"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['GET'])
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.add(user)
        db.session.commit()
        session['username'] = user.username

        return redirect("/secret")   
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user: 
            session['username'] = user.username
            return redirect(f"/users/{username}")
        else: 
            form.username.errors.append('Invalid username/password')
    
    return render_template("login.html", form=form)

@app.route('/secret', methods=['GET'])
def secret():
    if 'username' not in session:
        return redirect('/login')
    return "You made it!"

@app.route('/logout')
def logout():

    session.pop("username")
    return redirect("/login")

@app.route('/users/<username>')
def show_user(username):
    """user page for logged-in-users"""

    user = User.query.get(username)
    
    return render_template("users/show.html", user=user)