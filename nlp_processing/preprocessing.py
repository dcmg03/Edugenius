import spacy
from tqdm import tqdm
from flask_socketio import emit

# Descargar el modelo en_core_web_sm si no está instalado
def download_spacy_model():
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        spacy.load("en_core_web_sm")

# Asegurarse de que el modelo esté descargado
download_spacy_model()

# Cargar el modelo de spaCy
nlp = spacy.load("en_core_web_sm")

def classify_content(content, socketio):
    classified_content = {
        "historia": [],
        "matematica": [],
        "ingles": []
    }

    history_keywords = ["historia", "revolución", "guerra", "antigua", "medieval", "siglo", "descubrimiento", "imperio", "monarquía", "reinado", "colonia", "independencia", "civilización", "prehistoria", "edad media", "renacimiento", "barroco", "neoclásico", "moderno", "contemporáneo"]
    math_keywords = ["matemática", "álgebra", "geometría", "cálculo", "teorema", "ecuación", "aritmética", "trigonometría", "probabilidad", "estadística", "matriz", "determinante", "función", "derivada", "integral", "lógica", "conjunto", "número", "fracción", "decimal", "binario", "vector", "espacio", "punto", "recta"]
    english_keywords = ["inglés", "grammar", "vocabulary", "idiom", "language", "speaking", "listening", "reading", "writing", "pronunciation", "phonetics", "semantics", "lexicon", "slang", "idiom", "phrase", "conversation", "dialogue", "essay", "composition", "text", "report", "letter", "novel", "poem", "drama", "theater"]

    total_content = len(content)

    for i, doc in enumerate(tqdm(nlp.pipe(content), desc="Clasificación con spaCy", unit="doc", total=total_content)):
        try:
            if any(keyword in doc.text.lower() for keyword in history_keywords):
                classified_content["historia"].append(doc.text)
            elif any(keyword in doc.text.lower() for keyword in math_keywords):
                classified_content["matematica"].append(doc.text)
            elif any(keyword in doc.text.lower() for keyword in english_keywords):
                classified_content["ingles"].append(doc.text)

            progress = int((i + 1) / total_content * 100)
            socketio.emit('progress', {'category': 'clasificación', 'progress': progress})
        except Exception as e:
            print(f"Error procesando el documento {i}: {e}")

    return classified_content
