import spacy
from tqdm import tqdm
from flask_socketio import emit

nlp = spacy.load("es_core_news_sm")

def classify_content(content, socketio):
    classified_content = {
        "historia": [],
        "matematica": [],
        "ingles": []
    }

    history_keywords = ["historia", "revolución", "guerra", "antigua", "medieval", "siglo", "descubrimiento", "imperio", "monarquía", "reinado", "colonia", "independencia", "civilización", "prehistoria", "edad media", "renacimiento", "barroco", "neoclásico", "moderno", "contemporáneo"]
    math_keywords = ["matemática", "álgebra", "geometría", "cálculo", "teorema", "ecuación", "aritmética", "trigonometría", "probabilidad", "estadística", "matriz", "determinante", "función", "derivada", "integral", "lógica", "conjunto", "número", "fracción", "decimal", "binario", "vector", "espacio", "punto", "recta"]
    english_keywords = ["inglés", "grammar", "vocabulary", "idioma", "language", "speaking", "listening", "reading", "writing", "pronunciation", "phonetics", "syntax", "semantics", "lexicon", "slang", "idiom", "phrase", "conversation", "dialogue", "essay", "composition", "article", "report", "letter", "novel", "poem", "drama", "theater"]

    total_content = len(content)

    for i, doc in enumerate(tqdm(nlp.pipe(content), desc="Clasificación con spaCy", unit="doc", total=total_content)):
        if any(keyword in doc.text.lower() for keyword in history_keywords):
            classified_content["historia"].append(doc.text)
        elif any(keyword in doc.text.lower() for keyword in math_keywords):
            classified_content["matematica"].append(doc.text)
        elif any(keyword in doc.text.lower() for keyword in english_keywords):
            classified_content["ingles"].append(doc.text)
        
        progress = int((i + 1) / total_content * 100)
        socketio.emit('progress', {'category': 'clasificacion', 'progress': progress})

    return classified_content
