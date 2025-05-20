import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Sentiment Myfxbook", layout="wide")
st.title("📊 Sentiment des traders particuliers (Myfxbook)")

# Chargement du fichier CSV
@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

df = charger_donnees()

# Ajout d'une colonne 'Signal'
df["Signal"] = df.apply(
    lambda row: "✅ Achat" if row["% Achat"] >= 70 else (
        "❌ Vente" if row["% Vente"] >= 70 else "⚪️ Neutre"
    ),
    axis=1
)

# Affichage du tableau complet
st.subheader("Données brutes avec indicateur de signal")
st.dataframe(df, use_container_width=True)

# Filtrage
seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 70)
df_filtré = df[(df["% Achat"] >= seuil) | (df["% Vente"] >= seuil)]

st.subheader(f"🎯 Actifs filtrés (> {seuil}%)")
st.dataframe(df_filtré.reset_index(drop=True), use_container_width=True)

# === Graphique horizontal Achat vs Vente ===
if not df_filtré.empty:
    df_plot = df_filtré.sort_values(by="% Achat", ascending=True)

    fig, ax = plt.subplots(figsize=(10, len(df_plot) * 0.5))

    ax.barh(df_plot["Actif"], df_plot["% Achat"], label="% Achat", color='green')
    ax.barh(df_plot["Actif"], -df_plot["% Vente"], label="% Vente", color='red')

    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlabel("Pourcentage")
    ax.set_title("Comparatif Achat vs Vente")
    ax.legend(loc="upper right")

    st.pyplot(fig)
else:
    st.info("Aucun actif ne correspond au filtre.")
