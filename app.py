from flask import Flask, render_template, redirect, session, url_for, flash
from models import connect_db, db, User, bcrypt, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from functools import wraps

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authentication"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretauth"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

# toolbar = DebugToolbarExtension(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

        flash(f'{ username } registered!')
        return redirect("/login")   
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
    
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():

    session.pop("username")
    flash(f'See you next time!')
    return redirect(url_for('login'))

@app.route('/users/<username>')
@login_required
def show_user(username):
    """user page for logged-in-users"""

    user = User.query.get(username)

    if 'username' not in session or username != session['username']:
        flash(f'Not authorized')
        return redirect('/login')
    form = FeedbackForm()
    return render_template("users/show.html", user=user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
@login_required
def remove_user(username):

    if 'username' in session != session['username']:
        flash(f'Unauthorized')
        raise Exception("Unauthorized")
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect('/login')

@app.route('/users/<username>/feedback/new', methods=['GET', 'POST'])
@login_required
def new_feedback(username):
    """GET to display form to add feedback and POST to add a new piece of feedback and redirect to users/<username> -- only allow user who is logged in to add feedback"""
    
    # Check if the logged-in user matches the username in the URL
    if session.get('username') != username:
        flash("You don't have permission to access this page.", "danger")
        return redirect(url_for('home'))  # Redirect to a safer page
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username=username

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/new.html", username=username, form=form)
    
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
@login_required
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    """Make sure that only the user who has written that feedback can update it."""
    # Check if logged-in user matches username in URL otherwise flash no permissions message and redirect
    if 'username' not in session or feedback.username != session['username']: 
        flash("You don't have permission to access this page.", "danger")
        return redirect(url_for('home'))  # Redirect to a safer page
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    """Make sure that only the user who has written that feedback can delete it."""

    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']: 
        flash("You don't have permission to access this page.", "danger")
        return redirect(url_for('home'))  # Redirect to a safer page
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")