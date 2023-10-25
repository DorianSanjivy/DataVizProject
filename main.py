import base64
import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import json
import os
from bokeh.plotting import figure
from bokeh.palettes import Category20c
from math import pi
from bokeh.transform import cumsum

# Chargement des données
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

# Affichage de la barre latérale
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

    st.sidebar.markdown("---")

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

# Chargement des dataframes
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



# Analyse du Chiffre d'Affaires sur le marché du jeu vidéo
def plot_CA_analysis(df_ca):
    # Initialisation des données pour la visualisation
    annees = df_ca["Année"]
    ca_total = df_ca["Total"]
    ca_pc = df_ca["PC"]
    ca_console = df_ca["Console"]
    ca_mobile = df_ca["Mobile"]

    fig, ax1 = plt.subplots(figsize=(10,6))

    # Tracer le chiffre d'affaires total avec ax1
    ax1.set_xlabel('Année', color='black')
    ax1.set_ylabel('Chiffre d\'affaires Total (en M€)', color='black')
    ax1.plot(annees, ca_total, color='black', label='Chiffre d\'affaires Total', linewidth=2.5)
    ax1.tick_params(axis='y', labelcolor='black', colors='black')
    ax1.tick_params(axis='x', colors='black')

    # Pour s'assurer que les années sont présentées par année entière
    ax1.set_xticks(annees)

    # Tracer la segmentation sans un axe secondaire
    ax1.stackplot(annees, ca_pc, ca_console, ca_mobile, labels=['PC','Console','Mobile'], alpha=0.6)
    ax1.legend(loc='upper left')

    # Enlever les bords de l'axe
    for spine in ax1.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    plt.title('Analyse du Chiffre d\'Affaires sur le marché du jeu vidéo', color='black')
    st.pyplot(fig)


# Revenus par Genre de Jeu Vidéo
def plot_genre_analysis(df_genre_revenue):
    # Création d'un graphique à barres empilées avec Streamlit
    st.markdown("<h1 style='text-align: center;'>Revenus par Genre de Jeu Vidéo</h1>", unsafe_allow_html=True)

    # Extraire les années et les données par genre
    annees = df_genre_revenue["Année"].tolist()
    data_by_genre = df_genre_revenue.drop("Année", axis=1)

    # Convertir les données pour qu'elles soient compatibles avec le tracé de Streamlit
    df_long = pd.melt(df_genre_revenue, id_vars=['Année'], value_vars=data_by_genre.columns)

    # Créer le graphique à barres empilées avec un schéma de couleurs personnalisé
    bars = alt.Chart(df_long).mark_bar().encode(
        x=alt.X('Année:O', axis=alt.Axis(title='', labelAngle=0)),
        y=alt.Y('sum(value):Q', title="Revenus (en M€)"),
        color=alt.Color('variable:N', scale=alt.Scale(scheme='set2'), legend=alt.Legend(title="Genre")),
        order=alt.Order(
          # Ordre des bars par colonne
          'variable:N',
          sort='ascending'
        )
    )
    st.altair_chart(bars, use_container_width=True)



# Évolution du Prix Moyen des Jeux par Genre (Top 5 variations)
def plot_price_fluctuation_analysis(df_avg_price):
    # Création d'un dataframe pour stocker les variations de prix
    genres_prices = df_avg_price.drop('Année', axis=1)

    # Calculer la variation de prix pour chaque genre
    df_avg_price = df_avg_price.set_index('Année')  # Définir "Année" comme index pour faciliter les calculs
    variations = genres_prices.pct_change().sum().sort_values(ascending=False)

    # Sélectionner les 5 genres avec la plus grande variation
    top_genres_names = variations.head(5).index

    # Filtrer df_avg_price pour ne garder que les genres du Top 5
    df_top_genres = df_avg_price[top_genres_names].reset_index()

    # Transformer le dataframe pour le format long
    df_long = df_top_genres.melt('Année', var_name='Genre', value_name='Prix')

    # Afficher le titre
    st.title('Évolution du Prix Moyen des Jeux par Genre (Top 5 variations)')

    # Créer le graphique à ligne avec Altair
    chart = alt.Chart(df_long).mark_line().encode(
        x=alt.X('Année:O', title='Année', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Prix:Q', title='Prix en €'),
        color='Genre:N',
        tooltip=['Genre', 'Année', 'Prix']
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)



# Chiffre d'affaires par écosystème
def plot_CA_écosystème_analysis(df_ecosysteme_ca):
    # Définition des couleurs de base pour chaque plate-forme (couleurs pastel)
    base_colors = {
        'Console': (0.6, 0.8, 1),  # Bleu pastel
        'PC': (1, 0.6, 0.6),  # Rouge pastel
        'Mobile': (0.6, 1, 0.6)  # Vert pastel
    }

    # Définition des catégories pour chaque plate-forme
    platform_categories = {
        'Console': ["Matériel Console", "Accessoire Console", "Logiciel Physique Console",
                    "Logiciel Dématérialisé Console"],
        'PC': ["Matériel PC", "Accessoire PC", "Écrans PC", "Logiciel Physique PC", "Logiciel Dématérialisé PC"],
        'Mobile': ["Logiciel Mobile"]
    }

    # Fonction pour ajuster la luminosité d'une couleur
    def adjust_lightness(color, amount=0.5):
        import colorsys
        try:
            c = colorsys.rgb_to_hls(*color)
            return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
        except:
            return color

    # Création du graphique
    fig, ax = plt.subplots(figsize=(15, 8))

    # Pour stocker les hauteurs cumulatives
    height_cumulative = [0] * len(df_ecosysteme_ca['Année'])

    # Parcourir chaque plate-forme
    for platform, categories in platform_categories.items():
        base_color = base_colors[platform]

        # Parcourir chaque catégorie dans la plate-forme
        for i, category in enumerate(categories):
            # Ajuster la luminosité pour la catégorie
            category_color = adjust_lightness(base_color,
                                              amount=1 - i * 0.1)  # Réduire légèrement la luminosité pour chaque catégorie

            values = df_ecosysteme_ca[category]
            ax.bar(df_ecosysteme_ca['Année'], values, bottom=height_cumulative, color=category_color, label=category)

            # Mise à jour des hauteurs cumulatives
            height_cumulative = [h + v for h, v in zip(height_cumulative, values)]

    # Ajouter des éléments supplémentaires au graphique
    ax.set_title('Chiffre d\'affaires par écosystème')
    ax.set_ylabel('CA (M€)')

    # Inversion de l'ordre des légendes pour les aligner avec le graphique
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left', bbox_to_anchor=(1, 1))

    plt.xticks(df_ecosysteme_ca['Année'])
    plt.tight_layout()
    st.pyplot(plt)



# Répartition des jeux par classification PEGI
def plot_units_sold_PEGI_analysis(df_units):
    # Sélectionner l'année avec un slider
    selected_year = st.slider('Choisissez une année', 2016, 2021, 2016)

    # Filtrer le DataFrame selon l'année sélectionnée et exclure la colonne "Total"
    data_selected_year = df_units[df_units["Année"] == selected_year].drop(columns=["Année", "Total"]).T
    data_selected_year = data_selected_year.reset_index()
    data_selected_year.columns = ['PEGI', 'value']

    # Calculer les angles pour le graphique à secteurs
    data_selected_year['angle'] = data_selected_year['value']/data_selected_year['value'].sum() * 2*pi

    # Assigner des couleurs pour chaque segment
    data_selected_year['color'] = Category20c[len(data_selected_year)]

    # Calculer le pourcentage pour chaque classification PEGI
    data_selected_year['percentage'] = (data_selected_year['value'] / data_selected_year['value'].sum()) * 100

    # Créer le graphique à secteurs avec Bokeh
    p = figure(height=350, title=f"Répartition des jeux par classification PEGI ({selected_year})", toolbar_location=None,
               tools="hover", tooltips="@PEGI: (@percentage{0.1f}%)", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='PEGI', source=data_selected_year)

    # Désactiver les graduations des axes
    p.axis.visible = False
    st.bokeh_chart(p)



# Profit par unité selon la classification PEGI et l'année
def plot_profit_PEGI_analysis(df_units, df_sales):
    df_sales = df_sales.drop(columns=[ "Total"])
    df_units = df_units.drop(columns=[ "Total"])
    df_profit_per_unit = df_sales.copy()
    for column in df_profit_per_unit.columns:
        if column != "Année":
            df_profit_per_unit[column] = df_sales[column] / df_units[column]

    df_melted = df_profit_per_unit.melt(id_vars="Année", var_name="Classification PEGI", value_name="Profit par unité")

    # Création du graphique
    fig = px.line(df_melted, x="Année", y="Profit par unité", color="Classification PEGI", title="Profit par unité selon la classification PEGI et l'année", markers=True)

    st.plotly_chart(fig)



def main():
    # Titre de l'application
    st.title("Quelles sont les évolutions marquantes du marché du jeu vidéo, où se trouvent les opportunités à venir ?")
    display_sidebar_info()
    data = load_data()
    load_all_dataframes(data)

    plot_CA_analysis(df_ca)
    plot_genre_analysis(df_genre_revenue)
    plot_price_fluctuation_analysis(df_avg_price)
    plot_CA_écosystème_analysis(df_ecosysteme_ca)
    plot_units_sold_PEGI_analysis(df_units)
    plot_profit_PEGI_analysis(df_units, df_sales)

if __name__ == "__main__":
    main()


























