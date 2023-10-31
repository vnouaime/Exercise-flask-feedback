# Pet Adoption

Welcome to My Project! This project allows users create a profile for themselves and create feedback.  

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

To install and run My Project locally, please follow these steps:  

1. Navigate to desired local project directory:

cd YOUR-DIR  

2. Clone Repository:

https://github.com/vnouaime/Exercise-Pet-Adoption.git  

3. Create venv folder and activate virtual environment:

python -m venv venv  
source venv/bin/activate  

4. Install the dependencies:

pip install flask  
pip install Flask-DebugToolbar  
pip install python-dotenv  
pip install psycopg2-binary  
pip install flask-sqlalchemy  
pip install flask-wtf  
pip install flask-bcrypt   

5. Set up flask environment:

export FLASK_ENV=development  
export FLASK_ENV=testing  

6. Start the application:

flask run  

5. Open your web browser and visit `http://localhost:5000` to access My Project.

## Usage

Redirects to register page where user can register and will be redirected to their own new page. Displays username, email, first, and last name. Users can update and delete their own feedback from their page. Can only view other users with their feedback. Users can log out and log in where they are authenticated. Users can delete their own profile as well.  

## Contributing

Contributions are welcome! If you'd like to contribute to My Project, please follow these steps:  

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/my-feature`.
5. Submit a pull request.
 
