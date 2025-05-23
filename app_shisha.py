import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Fusion Shisha Monde", layout="centered")

st.title("🌍 Fusionneur de fichiers Shisha")

st.markdown("""
Cette application permet de **fusionner plusieurs fichiers Excel** contenant des données régionales Shisha 
et de produire un fichier maître sans doublons (basé sur les colonnes **Nom** et **Adresse**).
""")

uploaded_files = st.file_uploader("📤 Sélectionnez vos fichiers Excel :", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ {uploaded_file.name} chargé avec succès.")
            dfs.append(df)
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement de {uploaded_file.name} : {e}")

    if st.button("🔄 Fusionner les fichiers"):
        try:
            df_concat = pd.concat(dfs, ignore_index=True)

            df_concat['Nom_clean'] = df_concat['Nom'].str.strip().str.lower()
            df_concat['Adresse_clean'] = df_concat['Adresse'].str.strip().str.lower()

            df_final = df_concat.drop_duplicates(subset=['Nom_clean', 'Adresse_clean']).copy()
            df_final.drop(columns=['Nom_clean', 'Adresse_clean'], inplace=True)

            output = BytesIO()
            df_final.to_excel(output, index=False)
            output.seek(0)

            st.success("🎉 Fusion réussie !")
            st.download_button("📥 Télécharger le fichier fusionné", output, file_name="GMS_shisha_monde_maitre_complet.xlsx")
        except Exception as e:
            st.error(f"❌ Erreur pendant la fusion : {e}")