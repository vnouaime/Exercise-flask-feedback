from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SelectField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length, Email

class RegisterUserForm(FlaskForm): 
  """ Form for registering new user """

  username = StringField("Username", 
                          validators=[
                              Length(max=20, message="Username must be under 20 characters"),
                              InputRequired()
                            ])
  password = PasswordField("Password", 
                            validators=[InputRequired()])
  email = StringField("Email", 
                        validators=[
                          Email(message="Email not valid. Please enter a valid email"),
                          Length(max=50, message="Email must be under 50 characters"),
                          InputRequired()
                        ])
  first_name = StringField("First Name",
                            validators=[
                              Length(max=30, message="First name must be under 30 characters"),
                              InputRequired()
                            ])
  last_name = StringField("Last Name",
                            validators=[
                              Length(max=30, message="Last name must be under 30 characters"),
                              InputRequired()
                            ])

class LoginUserForm(FlaskForm):
  """ Form for logging in existing user """

  username = StringField("Username", 
                          validators=[InputRequired()])
  password = PasswordField("Password", 
                            validators=[InputRequired()])

class FeedbackForm(FlaskForm):
  """ Form for adding new feedback and updating """

  title = StringField("Title",
                       validators=[
                          Length(max=100, message="Title must be under 100 characters"),
                          InputRequired()
                        ])
  content = TextAreaField("Content",
                           validators=[InputRequired()])

class DeleteForm(FlaskForm):
  """ Deletes feedback """

