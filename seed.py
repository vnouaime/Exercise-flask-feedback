import os
from models import db, connect_db, User, Feedback
from app import app

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'

db.drop_all()
db.create_all()

User.query.delete()
Feedback.query.delete()

new_user = User.register(username="sallyshells", password="1234", email="sallyshells@gmail.com", first_name="Sally", last_name="Shells")
new_user_2 = User.register(username="leolab", password="5678", email="leolab@gmail.com", first_name="Leo", last_name="The Lab")

new_feedback_1 = Feedback(title="Test", content="Test123", user_username="sallyshells")
new_feedback_2 = Feedback(title="Test2", content="Test456", user_username="sallyshells")
new_feedback_3 = Feedback(title="Test3", content="Test789", user_username="leolab")
new_feedback_4 = Feedback(title="Test4", content="Test101112", user_username="leolab")

db.session.add_all([new_user, new_user_2, new_feedback_1, new_feedback_2, new_feedback_3, new_feedback_4])
db.session.commit()