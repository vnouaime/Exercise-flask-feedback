import os
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
    app.config['WTF_CSRF_ENABLED'] = False
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##################################################################################################################################
@app.route("/")
def home():
    """ Redirects to page to register a new user """

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ Gets form for registering user. If post request is successfull, 
    creates new user, and redirects to new user's page """

    if "user_username" in session:
        username = session["user_username"]
        flash("You are already logged in.")
        return redirect(f"/users/{username}")

    form = RegisterUserForm()
   
    if form.validate_on_submit(): 
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)

        db.session.add(new_user)
        try:
            db.session.commit()
            session["user_username"] = new_user.username
            flash(f'Welcome {new_user.username}! Successfully Created Your Account!')
            return redirect(f"/users/{new_user.username}")
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e):
                form.email.errors.append('This email is already registered with us. Please use a different one.')
            elif 'username' in str(e):
                form.username.errors.append('Username taken. Please pick another')
            return render_template('user_register.html', form=form)
    else:
        return render_template("user_register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user(): 
    """ Gets form for logging in. If post request is successful, 
    redirects logged in user to their own page """

    if "user_username" in session:
        username = session["user_username"]
        flash("You are already logged in.")
        return redirect(f"/users/{username}")

    form = LoginUserForm()

    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        
        if user:
            session["user_username"] = user.username
            flash(f"Welcome back, {user.first_name}! ")
            return redirect(f"/users/{user.username}")
        else: 
            flash("Invalid username/password")
            return render_template("user_login.html", form=form)

    else:
        return render_template("user_login.html", form=form)

@app.route('/logout')
def logout_user():
    """ Request to logout user and removes user from session  """
    
    if 'user_username' in session:
        session.pop('user_username')
        flash("Logout successful!")
    else:
        flash("You are not logged in.")

    return redirect('/login')

##################################################################################################################################
# User Routes
@app.route("/users/<string:username>")
def user_page(username):
    """ Displays user's page with information and feedback. Can only
    access if logged in """

    if "user_username" not in session:
        flash("Please login first!")
        return redirect("/login")
        
    user = User.query.get_or_404(username)
    user_feedback = Feedback.query.filter_by(user_username=user.username).all()
    form = DeleteForm()

    return render_template("user_page.html", user=user, user_feedback=user_feedback, form=form)

@app.route("/users/<string:username>/feedback/add", methods=["GET", "POST"])
def user_feedback_add(username):
    """ Gets form to add new feedback for user. If post request is successfull,
    creates new feedback """

    if "user_username" not in session:
        flash("Please login first!")
        return redirect("/login")

    user = User.query.get_or_404(username)
    form = FeedbackForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        data["user_username"] = user.username
        new_feedback = Feedback(**data)

        db.session.add(new_feedback)
        
        db.session.commit()
        flash("New Feedback Created!")
        return redirect(f"/users/{user.username}")
        
    else:
        return render_template("feedback_add.html", form=form)

@app.route("/users/<string:username>/delete", methods=["POST"])
def user_delete(username):
    """ Deletes logged in user from database. Cannot be done if not logged in or 
    if different user is in session """

    if "user_username" not in session:
        flash("Please login first!")
        return redirect("/login")

    user = User.query.get_or_404(username)

    if user.username != session["user_username"]:
        flash("You do not have permission to do this")
        return redirect(f"/users/{user.username}")

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        session.pop('user_username')
        flash("User Deleted!")
        return redirect("/")



##################################################################################################################################
# Feedback Routes

@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def feedback_update(id):
    """ Gets form for updating feedback. If post request successful, updates
    feedback """

    if "user_username" not in session:
        flash("Please login first!")
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)

    if feedback.user_username != session["user_username"]:
        flash("You do not have permission to do this")
        return redirect(f"/users/{feedback.user_username}")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        flash("Feedback has been updated!")
        return redirect(f"/users/{feedback.user_username}")

    return render_template("feedback_update.html", form=form)


@app.route("/feedback/<int:id>/delete", methods=["POST"])
def feedback_delete(id):
    """ Deletes feedback. Can only delete if logged in and creater
    of feedback is logged in """

    if "user_username" not in session:
        flash("Please login first!")
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)

    if feedback.user_username != session["user_username"]:
        flash("You do not have permission to do this")
        return redirect(f"/users/{feedback.user_username}")

    form = DeleteForm()
    
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback Deleted!")
        return redirect(f"/users/{session['user_username']}")
    
    
    
    
