# Scripts para tokenización, etiquetado, y análisis semántico con spaCy y NLTK
import spacy

nlp = spacy.load('en_core_web_sm')

def tokenize_text(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    return tokens
#que las respuestas no se repitan, tiene que ser generativos
