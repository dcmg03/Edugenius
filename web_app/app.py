from flask import Flask, request, render_template
from nlp_processing.preprocessing import tokenize_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    tokens = tokenize_text(text)
    return render_template('result.html', tokens=tokens)

if __name__ == '__main__':
    app.run(debug=True)
