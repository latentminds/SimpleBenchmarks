import streamlit as st


# model = st.query_params['model']

# st.write(model)

# streamlit_app.py
import os
import streamlit as st
import matplotlib.pyplot as plt
import json
import numpy as np
from io import BytesIO

# Fonction pour charger tous les objets JSON dans un dossier
# def load_valuation_objects(folder_path):
#     json_valuations = {}
#     for root, dirs, files in os.walk(os.path.abspath(folder_path)):
#         for file in files:
#             if file.endswith('.json') and "checkpoint" not in file:
#                 file_path = os.path.join(root, file)
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     json_valuations[file] = data
#     return json_valuations

#Fonction pour charger tous les objets JSON dans le dossier courant
def load_valuation_objects(folder_path):
    json_valuations = {}
    for file in os.listdir(folder_path):
        if file.endswith('.json') and "checkpoint" not in file:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_valuations[file] = data
    return json_valuations

# Fonction pour créer le graphique en étoile pour les traits de personnalité
def create_star_graph(traits, title):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))  # Réduire la taille du graphique
    traits_names = list(traits.keys())
    angles = np.linspace(0, 2 * np.pi, len(traits_names), endpoint=False).tolist()
    angles += angles[:1]
    values = list(traits.values())
    values += values[:1]
    ax.fill(angles, values, color='lightblue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits_names, fontsize=20)  # Réduire la taille de la police des labels
    return fig

# Fonction pour calculer la somme des scores pour chaque trait
def calculate_sum_scores(bigFiveResponseDict):
    return {trait: sum(scores) for trait, scores in bigFiveResponseDict.items()}

# Fonction pour créer des sliders dynamiques pour les traits
def create_sliders(sum_scores_dict, bigFiveResponseDict, filename, visibility="visible"):
    sliders = {}
    for trait, scores in bigFiveResponseDict.items():
        default_value = sum_scores_dict[trait] / len(scores) if len(scores) > 0 else 0
        sliders[trait] = st.sidebar.slider(
            trait, -2.0, 2.0, float(default_value), step=0.1, key=f"{filename}-{trait}", label_visibility=visibility)
        
    return sliders