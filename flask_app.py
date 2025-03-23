from flask import Flask, redirect, render_template, request, flash, url_for, session
from models import db, Student, Project, StudentProjectAssignment, ActivityLog
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
import os

# Load variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

# MySQL DB configuration using .env
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def home():
    role = session.get('role', 'guest')
    return render_template('home.html', role=role)

@app.route('/students')
def show_students():
    students = Student.query.all()
    return render_template('students.html', students=students, role='admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()

        print(email, password, student)

        if not student:
            print("in if statement")
            flash('User not found.', 'danger')
            return redirect(url_for('login'))

        if not student.password:
            return render_template('set_password.html', email=student.email)

        if check_password_hash(student.password, password):
            session['student_id'] = student.id
            session['role'] = 'student'
            return redirect(url_for('student_dashboard'))
        else:
            flash('Incorrect password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', role='guest')

@app.route('/set-password', methods=['POST'])
def set_password():
    email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return render_template('set_password.html', email=email)

    student = Student.query.filter_by(email=email).first()
    if not student:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    student.password = generate_password_hash(new_password)
    db.session.commit()

    flash('Password set successfully. You can now log in.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def student_dashboard():
    student_id = session.get('student_id')
    if not student_id:
        return redirect(url_for('login'))

    student = Student.query.get(student_id)
    assignments = StudentProjectAssignment.query.filter_by(student_id=student_id).all()
    active_projects = [a.project for a in assignments if not a.date_left_project]
    rank = calculate_student_rank(student_id)

    return render_template('dashboard_student.html', student=student, active_projects=active_projects, rank=rank)

@app.route('/my-projects')
def my_projects():
    student_id = session.get('student_id')
    if not student_id:
        return redirect(url_for('login'))

    assignments = StudentProjectAssignment.query.filter_by(student_id=student_id).all()
    return render_template('student_projects.html', assignments=assignments)

@app.route('/log-work', methods=['POST'])
def log_work():
    student_id = session.get('student_id')
    if not student_id:
        return redirect(url_for('login'))

    project_id = request.form['project_id']
    description = request.form['work_log']

    new_log = ActivityLog(
        student_id=student_id,
        project_id=project_id,
        activity_type='Daily Update',
        description=description,
        ist = pytz.timezone('Asia/Kolkata'),
        timestamp = datetime.now(ist)
    )
    db.session.add(new_log)
    db.session.commit()

    flash('Work log updated successfully!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/rankings')
def student_rankings():
    students = Student.query.all()
    rankings = [(s, calculate_student_rank(s.id)) for s in students]
    rankings.sort(key=lambda x: x[1])  # Assuming lower rank value = higher rank
    return render_template('student_rankings.html', rankings=rankings)

# Dummy rank calculator (replace with actual logic)
def calculate_student_rank(student_id):
    logs = ActivityLog.query.filter_by(student_id=student_id).count()
    return 100 - logs  # simplistic: more logs = higher rank

@app.route('/logout')
def logout():
    session.clear()
    flash("You’ve been logged out.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
