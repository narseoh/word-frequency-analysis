import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.util import ngrams

# Télécharger les stopwords en français si nécessaire
import nltk
nltk.download('stopwords')

# Liste des stopwords français
stop_words = set(stopwords.words('french'))

# Fonction pour récupérer et nettoyer le contenu d'une URL
def fetch_clean_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Supprimer les sections inutiles
    for tag in ['nav', 'menu', 'sidebar', 'footer', 'header', 'script', 'style']:
        for element in soup.find_all(tag):
            element.decompose()

    # Récupérer le texte brut
    text = soup.get_text(separator=' ')
    
    # Nettoyage du texte
    words = re.findall(r'\b\w+\b', text.lower())
    words = [word for word in words if word not in stop_words and len(word) > 1]

    return words

# Fonction pour compter les occurrences des mots
def word_count(words):
    return Counter(words)

# Fonction pour compter les bigrammes
def bigram_count(words):
    bigrams = ngrams(words, 2)
    return Counter(bigrams)

# Interface Streamlit
st.title("Analyse de contenu de pages web")

urls = st.text_area("Entrez les URLs (une par ligne)").split()

if st.button("Analyser"):
    for url in urls:
        words = fetch_clean_content(url)
        word_counts = word_count(words)
        bigram_counts = bigram_count(words)

        st.header(f"Analyse pour {url}")
        
        st.subheader("Nombre d'occurrences des mots")
        st.write(word_counts.most_common(10))
        
        st.subheader("Nombre d'occurrences des bigrammes")
        st.write(bigram_counts.most_common(10))
