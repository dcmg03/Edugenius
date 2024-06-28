# Implementación de sistemas de recomendación basados en contenido
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def recommend_content(documents, query):
    tfidf = TfidfVectorizer().fit_transform(documents)
    query_tfidf = tfidf.transform([query])
    cosine_similarities = linear_kernel(query_tfidf, tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    return related_docs_indices
