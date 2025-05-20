import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sentiment Forex combiné", layout="wide")
st.title("📊 Sentiment Forex – Barre combinée (style Myfxbook)")

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

df = charger_donnees()

# === Sélecteur d'actifs
actifs_disponibles = df["Actif"].tolist()
actifs_selectionnés = st.multiselect("🗂️ Sélectionne les actifs à afficher :", actifs_disponibles, default=actifs_disponibles)

# === Filtrage
df_filtré = df[df["Actif"].isin(actifs_selectionnés)]

# === Slider de filtre pour % min
seuil = st.slider("Afficher les actifs avec un % achat ou vente supérieur à :", 0, 100, 0)
df_filtré = df_filtré[(df_filtré["% Achat"] >= seuil) | (df_filtré["% Vente"] >= seuil)]

# === Fonction pour afficher une barre combinée
def barre_combinee(achat, vente):
    return f"""
    <div style="width:100%; height:18px; display:flex; background-color:#f0f0f0; border-radius:4px; overflow:hidden;">
        <div style="width:{achat}%; background-color:green;"></div>
        <div style="width:{vente}%; background-color:red;"></div>
    </div>
    """

st.markdown("### 💹 Affichage combiné Achat / Vente")

# === Affichage par ligne
for _, row in df_filtré.iterrows():
    st.markdown(f"**{row['Actif']}**", unsafe_allow_html=True)
    st.markdown(barre_combinee(row["% Achat"], row["% Vente"]), unsafe_allow_html=True)
    st.markdown(
        f"<span style='color:green;'>Achat : {row['% Achat']}%</span> &nbsp;&nbsp;&nbsp;"
        f"<span style='color:red;'>Vente : {row['% Vente']}%</span><hr>",
        unsafe_allow_html=True
    )
