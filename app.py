import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sentiment Myfxbook", layout="wide")

st.title("📊 Sentiment des traders particuliers (Myfxbook)")

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

df = charger_donnees()

# Afficher le tableau complet
st.subheader("Données brutes (29 actifs)")
st.dataframe(df, use_container_width=True)

# Slider pour filtrer
seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 70)

df_filtré = df[(df["% Achat"] >= seuil) | (df["% Vente"] >= seuil)]

st.subheader(f"🎯 Actifs filtrés (> {seuil}%)")
st.dataframe(df_filtré.reset_index(drop=True), use_container_width=True)
