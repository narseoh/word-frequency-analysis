import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Exclure les balises et classes spécifiées
    exclude_tags = ['nav', 'menu', 'breadcrumb', 'footer', 'sidebar', 'form']
    exclude_classes = ['nav', 'menu', 'breadcrumb', 'footer', 'sidebar', 'form']

    for tag in exclude_tags:
        for element in soup.find_all(tag):
            element.decompose()  # Supprimer l'élément du DOM

    for class_name in exclude_classes:
        for element in soup.find_all(class_=class_name):
            element.decompose()  # Supprimer l'élément du DOM

    # Extraire le texte nettoyé
    text = soup.get_text(separator=' ', strip=True)
    return text

# Titre de l'application
st.title('Outil de récupération de contenu textuel')

# Instructions pour l'utilisateur
st.write('Veuillez entrer des URLs, une par ligne :')

# Champ de texte pour entrer les URLs
urls_input = st.text_area('Entrée des URLs')

# Affichage des URLs saisies
if st.button('Afficher le contenu textuel'):
    urls = urls_input.split('\n')
    st.write('Voici le contenu textuel extrait de chaque URL :')
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                cleaned_text = get_clean_text(response.content)
                st.write(f"URL: {url}")
                st.write(cleaned_text[:500])  # Afficher les premiers 500 caractères du texte
            else:
                st.write(f"Impossible de récupérer le contenu de {url}. Code d'erreur: {response.status_code}")
        except Exception as e:
            st.write(f"Une erreur s'est produite lors de la récupération de {url}: {str(e)}")
