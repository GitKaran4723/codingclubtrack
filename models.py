from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=True)
    technical_skills = db.Column(db.Text)
    status = db.Column(db.String(50), default='Active')
    github_username = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    assignments = db.relationship('StudentProjectAssignment', backref='student', lazy=True)
    logs = db.relationship('ActivityLog', backref='student', lazy=True)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    tech_stack = db.Column(db.String(255))
    status = db.Column(db.String(50), default='Ongoing')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    project_head_id = db.Column(db.Integer)

    assignments = db.relationship('StudentProjectAssignment', backref='project', lazy=True)
    logs = db.relationship('ActivityLog', backref='project', lazy=True)

class StudentProjectAssignment(db.Model):
    __tablename__ = 'student_project_assignments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    role = db.Column(db.String(100))
    date_joined_project = db.Column(db.Date)
    date_left_project = db.Column(db.Date)
    contribution_desc = db.Column(db.Text)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    activity_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(100))
    location = db.Column(db.String(150))
    date = db.Column(db.Date)
    result = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

class StudentEventParticipation(db.Model):
    __tablename__ = 'student_event_participations'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    role = db.Column(db.String(100))
    award_won = db.Column(db.String(100))
    remarks = db.Column(db.Text)

class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
