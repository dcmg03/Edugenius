from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profile', lazy=True))
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    interests = db.Column(db.String(250), nullable=True)

class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref=db.backref('requests', lazy=True))
