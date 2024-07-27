import sys
import os
import concurrent.futures
from tqdm import tqdm

# Agrega el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import db, User, UserProfile, UserRequest
from data_extraction.scraper import get_all_content
from nlp_processing.preprocessing import classify_content
import datetime
import openai
import time

# Configuración de la clave API de OpenAI
openai.api_key = 'clave'

app = Flask(__name__, static_folder='static', static_url_path='/static')
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
database_path = os.path.join(instance_path, 'users.db')

# Crear el directorio 'instance' si no existe
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Crear el archivo de la base de datos si no existe
if not os.path.exists(database_path):
    open(database_path, 'w').close()

with app.app_context():
    db.create_all()

def fetch_and_classify_content():
    print("Iniciando el scraping de contenido...")
    all_content = get_all_content()
    print("Scraping completado. Iniciando la clasificación de contenido con spaCy...")
    classified_content = classify_content(all_content)
    print("Clasificación completada.")
    return classified_content

@app.route('/')
def index():
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(fetch_and_classify_content)
            classified_content = future.result()
        return render_template('index.html', classified_content=classified_content)
    except Exception as e:
        print(f"Error al cargar el contenido: {e}")
        return render_template('index.html', classified_content={"historia": [], "matematica": [], "ingles": []})

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return redirect(url_for('result', username=username))
        else:
            return "Credenciales inválidas, por favor intenta nuevamente."
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
            return "El usuario ya existe, Cambia las credenciales.."

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        new_profile = UserProfile(
            user_id=new_user.id,
            email=email,
            birthdate=datetime.datetime.strptime(birthdate, '%Y-%m-%d').date(),
            gender=gender,
            interests=interests
        )
        db.session.add(new_profile)
        db.session.commit()

        return redirect(url_for('result', username=username))
    return render_template('register.html')

@app.route('/result/<username>', methods=['GET', 'POST'])
def result(username):
    response = None
    if request.method == 'POST':
        question = request.form['question']
        response = get_gpt35_response(question)
    return render_template('result.html', username=username, response=response)

@app.route('/ask_question/<username>', methods=['POST'])
def ask_question(username):
    question = request.form['question']
    response = get_gpt35_response(question)
    user = User.query.filter_by(username=username).first()
    if user:
        new_request = UserRequest(user_id=user.id, request_text=question, response_text=response)
        db.session.add(new_request)
        db.session.commit()
    return render_template('result.html', username=username, response=response)

@app.route('/submit_request/<username>', methods=['POST'])
def submit_request(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_request = request.form['request']
        new_request = UserRequest(user_id=user.id, request_text=user_request)
        db.session.add(new_request)
        db.session.commit()
        return "Petición enviada con éxito."
    return "Usuario no encontrado."

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

def get_gpt35_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return "Lo siento, no puedo responder tu pregunta en este momento."

if __name__ == '__main__':
    app.run(debug=True)
