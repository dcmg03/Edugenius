from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profiles = db.relationship('UserProfile', backref='user', lazy=True)
    requests = db.relationship('UserRequest', backref='user', lazy=True)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    interests = db.Column(db.String(500), nullable=False)

class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=True)  # Asegúrate de que esta columna esté definida
