import streamlit as st

# Titre de l'application
st.title('Test')

# Instructions pour l'utilisateur
st.write('Veuillez entrer des URLs, une par ligne :')

# Champ de texte pour entrer les URLs
urls_input = st.text_area('Entrée des URLs')

# Affichage des URLs saisies
if st.button('Afficher les URLs'):
    urls = urls_input.split('\n')
    st.write('Voici les URLs que vous avez entrées :')
    for url in urls:
        st.write(url)
