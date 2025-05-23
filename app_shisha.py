import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Explorer les données Shisha", layout="wide")

st.title("🌍 Données Shisha Monde")
st.markdown("Fusionnez, explorez et filtrez les données GMS Shisha par région.")

uploaded_files = st.file_uploader("📤 Sélectionnez vos fichiers Excel :", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_excel(uploaded_file)
            dfs.append(df)
            st.success(f"{uploaded_file.name} chargé.")
        except Exception as e:
            st.error(f"Erreur : {e}")

    if dfs and st.button("🔄 Fusionner et afficher les données"):
        df_concat = pd.concat(dfs, ignore_index=True)

        df_concat['Nom_clean'] = df_concat['Nom'].str.strip().str.lower()
        df_concat['Adresse_clean'] = df_concat['Adresse'].str.strip().str.lower()

        df_final = df_concat.drop_duplicates(subset=['Nom_clean', 'Adresse_clean']).copy()
        df_final.drop(columns=['Nom_clean', 'Adresse_clean'], inplace=True)

        st.success("✅ Fusion terminée ! Voici les données :")

        # Filtres interactifs
        with st.expander("🔍 Filtres avancés"):
            col1, col2 = st.columns(2)
            with col1:
                pays = st.multiselect("Filtrer par pays :", options=df_final['Pays'].dropna().unique())
            with col2:
                ville = st.multiselect("Filtrer par ville :", options=df_final['Ville'].dropna().unique())

            if pays:
                df_final = df_final[df_final['Pays'].isin(pays)]
            if ville:
                df_final = df_final[df_final['Ville'].isin(ville)]

        st.dataframe(df_final, use_container_width=True)

        # Option de téléchargement
        output = BytesIO()
        df_final.to_excel(output, index=False)
        output.seek(0)
        st.download_button("📥 Télécharger les données filtrées", output, file_name="donnees_shisha_filtrees.xlsx")

        # Statistiques simples
        st.markdown("### 📊 Statistiques rapides")
        st.metric("Nombre total d'établissements", len(df_final))
        if 'Pays' in df_final.columns:
            st.bar_chart(df_final['Pays'].value_counts())