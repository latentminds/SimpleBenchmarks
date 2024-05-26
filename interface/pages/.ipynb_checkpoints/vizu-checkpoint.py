import os
import sys
import streamlit as st
from io import BytesIO

# Ajouter le chemin où se trouve le module helper
sys.path.append("/data/data/interface/pages")

# Importer les fonctions depuis le module helper
from helper import load_valuation_objects, create_star_graph, calculate_sum_scores, create_sliders

# Obtenir le modèle à partir des paramètres de la requête
model = st.query_params['model']

# Afficher le modèle sélectionné
if model:
    st.title(f"{model}")
else:
    st.error("""Aucun modèle sélectionné. Veuillez spécifier un modèle dans les paramètres de la requête.""")
    st.stop()

# Fonction principale pour afficher l'application Streamlit
def main():
    # Chemin du dossier contenant les fichiers JSON pour le modèle sélectionné
    folder_path = f'/data/data/results/valuations/{model}'

    # Charger les objets de valuation
    json_valuations = load_valuation_objects(folder_path)

    if not json_valuations:
        st.error(f"Aucun fichier de valuation trouvé pour le modèle {model}.")
        return
    
    sort = list(reversed(sorted(list(json_valuations.items()))))

    # Afficher le dernier fichier avec les sliders dans la barre latérale
    last_filename, last_bigFiveResponseDict = sort[0]
    
    
    # last_filename, last_bigFiveResponseDict = sorted(list(json_valuations.items()))[0]
        
    # Création de la barre latérale
    st.sidebar.title('BIG 5')
    
    # Calculer la somme des scores pour chaque trait
    sum_scores_dict = calculate_sum_scores(last_bigFiveResponseDict)
    
    # Créer des sliders pour les traits du Big Five avec des valeurs par défaut basées sur les scores sommaires
    traits = create_sliders(sum_scores_dict, last_bigFiveResponseDict, last_filename)
    fig = create_star_graph(traits, f'Big Five - {last_filename}')
    st.sidebar.pyplot(fig)

    # Zone principale
    st.markdown(f"""
    #### Analysis of different discrimination biases
    
    We created specifically engineered forms to explore discrimination biases in open source pre-trained models.
    Each form was submitted to {model} and this pages charts the global scores  
    
    *Click on details to see each answers to the prompt*""")
    
    # Initialiser un compteur pour la disposition
    counter = 0
    n_cols = 2
    cols = st.columns(n_cols)  # Créer 4 colonnes pour la disposition
    
    # Afficher les deux premiers fichiers de valuation dans la partie principale sans sliders
    for filename, bigFiveResponseDict in sort[1:]:
        sum_scores_dict = calculate_sum_scores(bigFiveResponseDict)
        fig = create_star_graph(sum_scores_dict, f'{filename}')
        
        with cols[counter % n_cols]:
            st.subheader(filename.split(".")[0])
            st.pyplot(fig)
            
            # Enregistrer le graphique en mémoire
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            page_url = f"""https://ominous-cod-777qq6x9q67cr7xx-8000.app.github.dev/interface/form/?questions=https%3A%2F%2Fominous-cod-777qq6x9q67cr7xx-8000.app.github.dev%2Fforms%2F{filename}&answers=https%3A%2F%2Fominous-cod-777qq6x9q67cr7xx-8000.app.github.dev%2Fresults%2Fprobabilities%2F{model}%2F{filename}"""
            st.page_link(page_url, label="Details")
            
        counter += 1

if __name__ == "__main__":
    main()
