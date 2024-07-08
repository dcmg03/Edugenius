from flask import Flask, render_template, request, redirect, url_for
from models import db, User, UserProfile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crea la base de datos y las tablas
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return redirect(url_for('result', username=username))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        interests = request.form.getlist('interests')
        interests = ', '.join(interests)

        if User.query.filter_by(username=username).first():
            return "Username already exists, please try another."
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            new_profile = UserProfile(user_id=new_user.id, email=email, birthdate=birthdate, gender=gender,
                                      interests=interests)
            db.session.add(new_profile)
            db.session.commit()

            return redirect(url_for('result', username=username))
    return render_template('register.html')


@app.route('/result/<username>')
def result(username):
    return render_template('result.html', username=username)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
