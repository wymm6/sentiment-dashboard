import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sentiment Myfxbook", layout="wide")
st.title("📊 Sentiment Forex – Vue séparée Achat / Vente")

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

df = charger_donnees()

# Slider de filtrage
seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 70)

# === Séparer Achat et Vente
df_achat = df[df["% Achat"] >= seuil].sort_values(by="% Achat", ascending=True)
df_vente = df[df["% Vente"] >= seuil].sort_values(by="% Vente", ascending=True)

# === Graphique Achats
if not df_achat.empty:
    st.subheader("✅ Actifs dominés par l'achat")
    fig_achat = px.bar(
        df_achat,
        x="% Achat",
        y="Actif",
        orientation="h",
        color_discrete_sequence=["green"],
        labels={"% Achat": "Pourcentage d'achat"},
        title="Pourcentage d'achat par actif"
    )
    st.plotly_chart(fig_achat, use_container_width=True)
else:
    st.info("Aucun actif avec un pourcentage d'achat supérieur au seuil.")

# === Graphique Ventes
if not df_vente.empty:
    st.subheader("❌ Actifs dominés par la vente")
    fig_vente = px.bar(
        df_vente,
        x="% Vente",
        y="Actif",
        orientation="h",
        color_discrete_sequence=["red"],
        labels={"% Vente": "Pourcentage de vente"},
        title="Pourcentage de vente par actif"
    )
    st.plotly_chart(fig_vente, use_container_width=True)
else:
    st.info("Aucun actif avec un pourcentage de vente supérieur au seuil.")
