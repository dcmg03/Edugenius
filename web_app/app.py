from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data
users = {
    "user1": "password1",
    "user2": "password2"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('result', username=username))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists, please try another."
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/result/<username>')
def result(username):
    return render_template('result.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
