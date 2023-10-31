from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """ Connect to a database """
    db.app = app
    db.init_app(app)

class Feedback(db.Model):
    """ Creates new feedback with title, content, and foreign key to user """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_username = db.Column(db.String(), db.ForeignKey('users.username'))

class User(db.Model):
    """ Models a user in the database """

    __tablename__ = "users"
    
    username = db.Column(db.String(20), nullable=False, primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref="user", cascade="all, delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct. Return user if valid; else return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False