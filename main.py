import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@st.cache_data
def load_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'data.json')

    # Lire le fichier JSON
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data


def display_sidebar_info():
    # Barre latérale
    st.sidebar.title("#datavz2023efrei")

    # Lien vers la source des données avec une icône
    st.sidebar.markdown(
        "[:link: **Source CNC**](https://www.data.gouv.fr/fr/datasets/marche-du-jeu-video/)"
    )

    st.sidebar.markdown("---")  # Ajoute une ligne de séparation

    # Informations personnelles
    st.sidebar.markdown("## SANJIVY Dorian")
    st.sidebar.markdown("Promo 2025 - BI2")

    st.sidebar.markdown("---")  # Ajoute une ligne de séparation

    # Logos + Lien vers des réseaux
    current_directory = os.path.dirname(os.path.realpath(__file__))
    linkedin_path = os.path.join(current_directory, 'linkedin-logo.png')
    github_path = os.path.join(current_directory, 'github-logo.png')

    linkedin_url = "https://www.linkedin.com/in/dorian-sanjivy/"
    github_url = "https://github.com/DorianSanjivy"

    linkedin_logo_base64 = get_image_base64(linkedin_path)
    github_logo_base64 = get_image_base64(github_path)

    logos_markdown = f'''
    <a href="{linkedin_url}" target="_blank"><img src="data:image/png;base64,{linkedin_logo_base64}" width="64"></a>
    &nbsp; &nbsp; <!-- Double espace HTML pour un meilleur espacement entre les logos -->
    <a href="{github_url}" target="_blank"><img src="data:image/png;base64,{github_logo_base64}" width="64"></a>
    '''

    st.sidebar.markdown(logos_markdown, unsafe_allow_html=True)


def load_all_dataframes(data):
    global df_ca, df_repartition, df_segment_ca, df_segment_repartition, df_ecosysteme_ca, df_ecosysteme_repartition
    global df_supports_chiffre_affaires, df_supports_repartition, df_genre_units, df_genre_revenue
    global df_market_share, df_avg_price, df_units, df_sales, df_sales_distribution, df_avg_price_pegi

    df_ca = pd.DataFrame(data["ca_data_support"])
    df_repartition = pd.DataFrame(data["pourcentage_ca_support_repartition_data"])
    df_segment_ca = pd.DataFrame(data["data_segment_ca"])
    df_segment_repartition = pd.DataFrame(data["data_segment_repartition"])
    df_ecosysteme_ca = pd.DataFrame(data["data_ecosysteme_ca"])
    df_ecosysteme_repartition = pd.DataFrame(data["data_ecosysteme_repartition_ca"])
    df_supports_chiffre_affaires = pd.DataFrame(data["data_jeu_supports_chiffre_affaires"])
    df_supports_repartition = pd.DataFrame(data["data_supports_repartition_jeu_ca"])
    df_genre_units = pd.DataFrame(data["data_genre_units"])
    df_genre_revenue = pd.DataFrame(data["data_genre_revenue"])
    df_market_share = pd.DataFrame(data["data_market_share"])
    df_avg_price = pd.DataFrame(data["data_avg_price_type"])
    df_units = pd.DataFrame(data["data_units_pegi"])
    df_sales = pd.DataFrame(data["data_sales_pegi"])
    df_sales_distribution = pd.DataFrame(data["data_sales_distribution_pegi"])
    df_avg_price_pegi = pd.DataFrame(data["data_avg_price_age_pegi"])

display_sidebar_info()
data = load_data()
load_all_dataframes(data)

# Titre de l'application
st.title("Analyse du marché du jeu vidéo de 2016 à 2021")

# Introduction ou texte explicatif
st.write("""
Explorons ensemble les tendances, les ventes et l'évolution du marché du jeu vidéo pendant ces années !
""")

# Sélection de l'année
year = st.sidebar.slider('Choisir une année', 2017, 2021, 2017)

# Affichage des données de chiffre d'affaires pour l'année sélectionnée
st.subheader(f"Chiffre d'affaires en {year} (M€)")
st.bar_chart(df_ca.set_index("Année").loc[year])

# Affichage de la répartition pour l'année sélectionnée
st.subheader(f"Répartition du chiffre d'affaires en {year} (%)")
st.bar_chart(df_repartition.set_index("Année").loc[year])

# Visualisation du chiffre d'affaires selon le segment
st.subheader(f"Chiffre d'affaires selon le segment en {year} (M€)")
st.bar_chart(df_segment_ca.set_index("Année").loc[year])

# Visualisation de la répartition du chiffre d'affaires selon le segment
st.subheader(f"Répartition du chiffre d'affaires selon le segment en {year} (%)")
st.bar_chart(df_segment_repartition.set_index("Année").loc[year])

# Visualisation du chiffre d'affaires selon le segment et l'écosystème
st.subheader(f"Chiffre d'affaires selon le segment et l'écosystème en {year} (M€)")
st.bar_chart(df_ecosysteme_ca.set_index("Année").loc[year])

# Visualisation de la répartition du chiffre d'affaires selon le segment et l'écosystème
st.subheader(f"Répartition du chiffre d'affaires selon le segment et l'écosystème en {year} (%)")
st.bar_chart(df_ecosysteme_repartition.set_index("Année").loc[year])

st.subheader("Chiffre d’affaires du marché des jeux vidéo selon les supports de lecture (M€)")
fig, ax = plt.subplots()
df_supports_chiffre_affaires.set_index("Année").plot(kind="bar", ax=ax)
plt.title('Chiffre d’affaires par support de lecture (M€)')
plt.ylabel('Chiffre d’affaires (M€)')
plt.tight_layout()
st.pyplot(fig)

st.subheader("Répartition du chiffre d'affaires des ventes de jeux vidéo selon les supports de lecture (%)")
fig2, ax2 = plt.subplots()
df_supports_repartition.set_index("Année").plot(kind="bar", ax=ax2)
plt.title('Répartition par support de lecture (%)')
plt.ylabel('Pourcentage (%)')
plt.tight_layout()
st.pyplot(fig2)


st.title("Marché des jeux vidéo console selon le genre")

st.subheader("Marché des jeux vidéo console selon le genre (milliers d’unités)")

fig, ax = plt.subplots(figsize=(12,6))
df_genre_units.set_index("Année").plot(kind="bar", ax=ax)
plt.title('Marché des jeux vidéo console selon le genre (milliers d’unités)')
plt.ylabel('Nombre d’unités (en milliers)')
plt.tight_layout()
st.pyplot(fig)

st.subheader("Chiffre d’affaires du marché des jeux vidéo console selon le genre (M€)")

fig2, ax2 = plt.subplots(figsize=(12,6))
df_genre_revenue.set_index("Année").plot(kind="bar", ax=ax2)
plt.title('Chiffre d’affaires selon le genre (M€)')
plt.ylabel('Chiffre d’affaires (M€)')
plt.tight_layout()
st.pyplot(fig2)


# Les dataframes df_market_share et df_avg_price doivent être définis ici ou importés

st.title("Parts de marché et prix moyen des jeux vidéo console selon le genre")

st.subheader("Parts de marché des jeux vidéo console selon le genre (%)")

fig, ax = plt.subplots(figsize=(12,6))
df_market_share.set_index("Année").plot(kind="bar", ax=ax)
plt.title('Parts de marché des jeux vidéo console selon le genre (%)')
plt.ylabel('Parts de marché (%)')
plt.tight_layout()
st.pyplot(fig)

st.subheader("Prix moyen des jeux vidéo console selon le genre (€)")

fig2, ax2 = plt.subplots(figsize=(12,6))
df_avg_price.set_index("Année").plot(kind="bar", ax=ax2)
plt.title('Prix moyen des jeux vidéo console selon le genre (€)')
plt.ylabel('Prix moyen (€)')
plt.tight_layout()
st.pyplot(fig2)


# Les DataFrames df_units, df_sales, df_sales_distribution, et df_avg_price ont été définis précédemment.

st.title("Marché du jeu vidéo console selon la classification PEGI")

# Afficher et visualiser les données des milliers d’unités
st.subheader("Le marché des jeux vidéo console selon la classification PEGI (milliers d’unités)")

fig1, ax1 = plt.subplots(figsize=(12, 6))
df_units.set_index("Année").drop(columns=["Total"]).plot(kind="bar", ax=ax1)
plt.title("Le marché des jeux vidéo console selon la classification PEGI (milliers d’unités)")
plt.tight_layout()
st.pyplot(fig1)

# Afficher et visualiser le chiffre d’affaires
st.subheader("Chiffre d’affaires du marché des jeux vidéo console selon la classification PEGI (M€)")

fig2, ax2 = plt.subplots(figsize=(12, 6))
df_sales.set_index("Année").drop(columns=["Total"]).plot(kind="bar", ax=ax2)
plt.title("Chiffre d’affaires du marché des jeux vidéo console selon la classification PEGI (M€)")
plt.tight_layout()
st.pyplot(fig2)

# Afficher et visualiser la répartition du chiffre d'affaires
st.subheader("Répartition du chiffre d'affaires des jeux vidéo console selon la classification PEGI (%)")

fig3, ax3 = plt.subplots(figsize=(12, 6))
df_sales_distribution.set_index("Année").drop(columns=["Total"]).plot(kind="bar", stacked=True, ax=ax3)
plt.title("Répartition du chiffre d'affaires des jeux vidéo console selon la classification PEGI (%)")
plt.tight_layout()
st.pyplot(fig3)

# Afficher et visualiser le prix moyen
st.subheader("Prix moyen des jeux vidéo console selon la classification PEGI (€)")

fig4, ax4 = plt.subplots(figsize=(12, 6))
df_avg_price_pegi.set_index("Année").drop(columns=["Total"]).plot(kind="bar", ax=ax4)
plt.title("Prix moyen des jeux vidéo console selon la classification PEGI (€)")
plt.tight_layout()
st.pyplot(fig4)


