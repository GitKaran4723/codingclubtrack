from flask import Flask, render_template_string
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

# Route to display all students
@app.route('/')
def home():
    students = Student.query.all()
    return render_template_string("""
        <h2>Student List</h2>
        <table border="1" cellpadding="5">
            <tr>
                <th>ID</th><th>Name</th><th>Email</th><th>Skills</th><th>Status</th><th>GitHub</th><th>Date Joined</th>
            </tr>
            {% for student in students %}
            <tr>
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.email }}</td>
                <td>{{ student.technical_skills }}</td>
                <td>{{ student.status }}</td>
                <td>{{ student.github_username }}</td>
                <td>{{ student.date_joined.strftime('%Y-%m-%d %H:%M') }}</td>
            </tr>
            {% endfor %}
        </table>
    """, students=students)

if __name__ == '__main__':
    app.run(debug=True)
