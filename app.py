import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Sentiment Myfxbook", layout="wide")
st.title("📊 Sentiment des traders particuliers")

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

df = charger_donnees()

st.markdown("### 🔍 Données brutes")

# Construction du tableau interactif stylé
gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_column("% Achat", type=["numericColumn"], cellStyle={"color": "green"})
gb.configure_column("% Vente", type=["numericColumn"], cellStyle={"color": "red"})


gb.configure_default_column(editable=False, filter=True, sortable=True)

grid_options = gb.build()
AgGrid(df, gridOptions=grid_options, use_container_width=True)

# 🎯 Filtrage
st.markdown("### 🎯 Filtrer les extrêmes")
seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 70)
df_filtré = df[(df["% Achat"] >= seuil) | (df["% Vente"] >= seuil)]

st.markdown(f"### ✅ Résultats filtrés (> {seuil}%)")
AgGrid(df_filtré.reset_index(drop=True), gridOptions=gb.build(), use_container_width=True)
