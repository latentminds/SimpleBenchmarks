import streamlit as st


model = st.query_params['model']

st.write(model)


import sys
 
# setting path
sys.path.append('/data/pages')
 
# importing

from helper import *





# Fonction principale pour afficher l'application Streamlit

# Chemin du dossier contenant les fichiers JSON
folder_path = f'/data/data/results/valuations/{model}'




# Charger les objets de valuation
json_valuations = load_valuation_objects(folder_path)

filename, bigFiveResponseDict = list(json_valuations.items())[-1]


# Création de la barre latérale
st.sidebar.title('BIG 5')

# Zone principale
st.title('Big Five Personality Traits Analysis')
st.write('Cette application analyse les traits de personnalité du Big Five pour différents ensembles de données.')

# Initialiser un compteur pour la disposition
counter = 0
cols = st.columns(4)  # Créer 4 colonnes pour la disposition

json_valuations.items()

st.sidebar.header(f"{model}_{filename}")



# Calculer la somme des scores pour chaque trait
sum_scores_dict = calculate_sum_scores(bigFiveResponseDict)


# Créer des sliders pour les traits du Big Five avec des valeurs par défaut basées sur les scores sommaires
traits = create_sliders(sum_scores_dict, bigFiveResponseDict, filename)
fig = create_star_graph(traits, f'Big Five - {filename}')
st.sidebar.pyplot(fig)

# st.write(f"{traits} ______")

# Pour chaque fichier chargé, créer une section
for filename, bigFiveResponseDict in list(json_valuations.items())[:-1]:

    sum_scores_dict = calculate_sum_scores(bigFiveResponseDict)


    # Créer et afficher le graphique en étoile pour le fichier actuel
    traits = create_sliders(sum_scores_dict, bigFiveResponseDict, filename, visibility="collapsed")

    fig = create_star_graph(traits, f'{filename}')

    # Ajouter le graphique dans la zone principale dans une des colonnes
    with cols[counter % 2]:
        st.subheader(filename)
        st.pyplot(fig)
        # Enregistrer le graphique en mémoire
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.download_button(
            label="Télécharger le graphique",
            data=buf,
            file_name=f"{filename}.png",
            mime="image/png"
        )
        st.markdown(f"<p style='font-size:10px;'>Description du fichier {filename}</p>", unsafe_allow_html=True)

    counter += 1
