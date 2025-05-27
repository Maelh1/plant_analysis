import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Nature & Design - Paysagiste", 
    page_icon="🌿"
)

def get_inaturalist_image(plant_name):
    url = f"https://api.inaturalist.org/v1/search?q={plant_name}&sources=taxa"
    
    try:
        response = requests.get(url)
        data = response.json()

        # Vérifie s’il y a au moins un résultat avec une image
        results = data.get("results", [])
        if results:
            taxon = results[0].get("record", {})
            photo = taxon.get("default_photo", {})
            return photo.get("medium_url")  # Tu peux aussi essayer "large_url"
    except:
        return None  # Si erreur API ou pas d’image

    return None

def afficher_top5_plantes(df,selection):
    """
    Affiche le top 5 des plantes avec les meilleures notes
    """
    st.title(f"🌱 Top 5 des Meilleures Plantes pour {selection}")
    
    # Trier par Note en ordre décroissant et prendre les 5 premiers
    top5 = df.sort_values(by='Note', ascending=False).head(5)
    print(top5)
    
    # Afficher chaque plante
    for index, row in top5.iterrows():
        # Créer une colonne pour organiser l'affichage
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Afficher la photo si elle existe
            
            try:
                plante = row['Plante']
                photo = get_inaturalist_image(plante)
                st.image(photo, width=200)
            except:
                    # st.write("📷 Photo non disponible")
                st.image("plante_image.png", width=200)
        
        with col2:
            # Afficher le nom de la plante
            st.subheader(f"🌿 {row['Plante']}")
            
            # Afficher les détails
            st.write("**Détails:**")
            st.write(row['Details'])
            
            # Afficher la note avec des étoiles
            note = row['Note']
            etoiles = "⭐" * int(note) 
            st.write(f"**Évaluation:** {note}/10 {etoiles}")
        
        # Ligne de séparation
        st.divider()


villes_df = pd.read_csv("villes_bretagne.csv")
villes = villes_df["nom_standard"].sort_values()
dep_plants_csv = ["Côtes-d’Armor (22)_plantes.csv","Finistère (29)_plantes.csv","Ille-et-Vilaine (35)_plantes.csv","Loire-Atlantique (44)_plantes.csv","Morbihan (56)_plantes.csv"]

st.title("Quelles sont les meilleures plantes d'intérieur à planter dans mon jardin ?")
selection = st.selectbox(label = "Entrez votre ville", options = villes, index = None )
choose = st.button("Quelles plantes choisir")

if choose:
    #Selection du csv
    num_dep = villes_df[villes_df["nom_standard"] == selection]["dep_code"]
    num_dep = int(num_dep)
    for i in dep_plants_csv:
        if str(num_dep) in i:
            df_plant = pd.read_csv("csv_regions_plantes/"+i, sep=";")
            # df_plant= df_plant["Note"].astype(int)
            # st.dataframe(df_plant)


            break

    df_plant = df_plant.sort_values("Note")
    
    afficher_top5_plantes(df_plant,selection)
