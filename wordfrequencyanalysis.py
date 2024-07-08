import streamlit as st
import requests
from bs4 import BeautifulSoup

# Fonction pour extraire le contenu textuel d'une URL en filtrant les éléments non pertinents
def extract_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Liste des noms de classes et IDs à exclure
        excluded_classes = ['nav', 'breadcrumb', 'menu', 'footer', 'sidebar']
        excluded_ids = ['form']
        
        # Supprimer les éléments non pertinents en fonction des classes et IDs
        for tag in soup.find_all(True, {'class': excluded_classes, 'id': excluded_ids}):
            tag.decompose()
        
        # Extraire le texte restant
        text = soup.get_text(separator='\n')
        return text.strip()
    
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération de l'URL : {e}"

# Titre de l'application
st.title('Outil de récupération de contenu textuel')

# Instructions pour l'utilisateur
st.write('Veuillez entrer des URLs, une par ligne :')

# Champ de texte pour entrer les URLs
urls_input = st.text_area('Entrée des URLs')

# Affichage des URLs saisies
if st.button('Afficher le contenu textuel des URLs'):
    urls = urls_input.split('\n')
    for url in urls:
        if url.strip():
            st.subheader(f"Contenu de l'URL : {url}")
            content = extract_content(url)
            st.write(content)
            st.markdown('---')  # Séparateur visuel entre les résultats
