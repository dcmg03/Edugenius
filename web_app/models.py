from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    age = db.Column(db.Integer)
    interests = db.Column(db.String(200))
    education_level = db.Column(db.String(50))
    email = db.Column(db.String(120), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<UserProfile {self.user.username}>'
