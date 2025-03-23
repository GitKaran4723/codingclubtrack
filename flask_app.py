from flask import Flask, render_template_string, render_template
from models import db, Student
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

app = Flask(__name__)

# MySQL DB configuration using .env
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def home():
    role = 'guest'  # simulate different roles like 'admin', 'student'
    return render_template('home.html', role=role)

@app.route('/students')
def show_students():
    students = Student.query.all()
    role = 'admin'
    return render_template('students.html', students=students, role=role)

if __name__ == '__main__':
    app.run(debug=True)
