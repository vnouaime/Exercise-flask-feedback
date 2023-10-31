from unittest import TestCase
from app import app
from flask import session, flash
from models import db, connect_db, User, Feedback
from forms import *
from wtforms import HiddenField

class FlaskTests(TestCase): 
    
    def setUp(self): 
        """Set up the Flask app for testing."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True 
        db.create_all()

    def tearDown(self): 
        """ Closes current session of database """ 
        db.session.close()

    #########################################################################################################################
    def test_home_page(self):
        """ Testing home page route """
        with app.test_client() as client:
            response = client.get("/")

            self.assertEqual(response.status_code, 302)

    def test_register_user(self):
        """ Testing get request of register user route """ 
        with app.test_client() as client:
            response = client.get("/register")
            html = response.get_data(as_text=True)
            form = RegisterUserForm()

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-1 text-center mt-3">Register</h1>', html)
            self.assertIn('<p class="lead text-center">Register below to join our application!</p>', html)

            for field in form: 
                if not isinstance(field, HiddenField):
                    self.assertIn(f'{field.label}', html)
                    self.assertIn(f'{field(class_="form-control")}', html)

    def test_register_post(self):
        """ Testing post request of register user route """
        with app.test_client() as client: 
            data = {
                'username': 'Vera', 
                'password': 'hello', 
                'email': 'nouaimevera@gmail.com', 
                'first_name': 'Vera',
                'last_name': 'Nouaime'
                }

            response = client.post('/register', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome Vera! Successfully Created Your Account!'.encode(), response.data)
            self.assertIn('<p class="card-text" style="font-size: 20px;">Username: Vera</p>', html)
            self.assertIn('<p class="card-text" style="font-size: 20px;">Email: nouaimevera@gmail.com</p>', html)
            self.assertIn('<h3 class="display-3">Feedback</h3>', html)

    def test_login(self):
        """ Testing get request of login route """
        with app.test_client() as client: 
            response = client.get("/login")
            html = response.get_data(as_text=True)
            form = LoginUserForm()

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-1 text-center mt-3">Login</h1>', html)
            self.assertIn('<p class="lead text-center">Login Below. Do not have an account? <a href="/register">Register Here</a></p>', html)

            for field in form: 
                if not isinstance(field, HiddenField):
                    self.assertIn(f'{field.label}', html)
                    self.assertIn(f'{field(class_="form-control")}', html)

    def test_login_post(self):
        """ Testing post request of login route """
        with app.test_client() as client:
            data = {"username": "sallyshells", "password": "1234"}

            response = client.post('/login', data=data, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """ Testing logout route """
        with app.test_client() as client: 
            response = client.get("/logout")

            self.assertEqual(response.status_code, 302)
    ##############################################################################################################################
    # User Route Tests
    def test_user_page(self):
        """ Testing get request of user route """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'sallyshells'

            response = client.get("/users/sallyshells", follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<p class="card-text" style="font-size: 20px;">Username: sallyshells</p>', html)
            self.assertIn('<p class="card-text" style="font-size: 20px;">Email: sallyshells@gmail.com</p>', html)
            self.assertIn('<h3 class="display-3">Feedback</h3>', html)

    def test_feedback_add(self):
        """ Testing get request of add feedback route """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'sallyshells'
            
            response = client.get("/users/sallyshells/feedback/add")
            html = response.get_data(as_text=True)
            form = FeedbackForm()

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-1 text-center mt-3">Add Feedback</h1>', html)

            for field in form: 
                if not isinstance(field, HiddenField):
                    self.assertIn(f'{field.label}', html)
                    self.assertIn(f'{field(class_="form-control")}', html)

    def test_feedback_add_post(self):
        """ Testing post request of add feedback route """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'sallyshells'

            data = {"title": "First Post", "content": "This is my first post!", "user_username": "sallyshells"}

            response = client.post("/users/sallyshells/feedback/add", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('New Feedback Created!'.encode(), response.data)
            self.assertIn('<h3 class="display-3">Feedback</h3>', html)
            self.assertIn('<a class="btn btn-sm btn-primary" href="/feedback/1/update">Update</a>', html)
            self.assertIn(' <button \n                      class="btn btn-sm btn-danger">Delete Feedback\n                    </button>', html)

    def test_user_delete(self):
        """ Testing post request of deleting user route """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'leolab'

            response = client.post("/users/leolab/delete", follow_redirects=True)
            html = response.get_data(as_text=True)
            form = RegisterUserForm()    
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('User Deleted!'.encode(), response.data)
            self.assertIn('<h1 class="display-1 text-center mt-3">Register</h1>', html)
            self.assertIn('<p class="lead text-center">Register below to join our application!</p>', html)

            for field in form: 
                if not isinstance(field, HiddenField):
                    self.assertIn(f'{field.label}', html)
                    self.assertIn(f'{field(class_="form-control")}', html)
    ##############################################################################################################################
    # Feedback Route Tests
    def test_feedback_update(self):
        """ Testing get request of updating feedback route """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'sallyshells'
            
            feedback = Feedback.query.get(1)
            response = client.get(f"/feedback/{feedback.id}/update")
            html = response.get_data(as_text=True)
            form = FeedbackForm(obj=feedback)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-1 text-center mt-3">Update Feedback</h1>', html)

            for field in form: 
                if not isinstance(field, HiddenField):
                    self.assertIn(f'{field.label}', html)
                    self.assertIn(f'{field(class_="form-control")}', html)

    def test_feedback_update_post(self):
        """ Testing post request of updating feedback route """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'sallyshells'

            feedback = Feedback.query.get(1)
            data = {"title": "Updated Post", "content": "Updated Test123", "user_username": "sallyshells"}
            response = client.post(f"/feedback/{feedback.id}/update", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f"Feedback has been updated!".encode(), response.data)
            self.assertIn('<h3 class="display-3">Feedback</h3>', html)
            self.assertIn('<a class="btn btn-sm btn-primary" href="/feedback/1/update">Update</a>', html)
            self.assertIn(' <button \n                      class="btn btn-sm btn-danger">Delete Feedback\n                    </button>', html)

    def test_feedback_delete(self):
        """ Testing post request of deleting feedback """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user_username'] = 'sallyshells'
            
            feedback = Feedback.query.get(2)
            response = client.post(f"/feedback/{feedback.id}/delete", follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f"Feedback Deleted!".encode(), response.data)




            