import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams

# Télécharger les stopwords en français si nécessaire
nltk.download('stopwords')

# Liste des stopwords français
stop_words = set(stopwords.words('french'))

# Fonction pour récupérer et nettoyer le contenu d'une URL
def fetch_clean_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifier si la requête a réussi
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération de l'URL {url}: {e}")
        return []

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
    if not urls:
        st.error("Veuillez entrer au moins une URL.")
    else:
        for url in urls:
            st.write(f"Récupération et analyse de {url}...")
            words = fetch_clean_content(url)
            if words:
                word_counts = word_count(words)
                bigram_counts = bigram_count(words)

                st.header(f"Analyse pour {url}")
                
                st.subheader("Nombre d'occurrences des mots")
                st.write(word_counts.most_common(10))
                
                st.subheader("Nombre d'occurrences des bigrammes")
                st.write(bigram_counts.most_common(10))
            else:
                st.warning(f"Aucun contenu récupéré pour {url}")
