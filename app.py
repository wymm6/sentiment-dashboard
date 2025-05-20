# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyse de Marché", layout="wide")
st.title("🧭 Tableau de bord marché – Forex & COT")

# === Navigation principale
onglet = st.sidebar.radio("📂 Choisis une catégorie :", ["📊 Sentiment Forex", "📄 Rapport COT"])

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

# === Onglet 1 : Sentiment Forex
if onglet == "📊 Sentiment Forex":
    st.subheader("📊 Sentiment Forex – Traders particuliers")

    df = charger_donnees()

    # Sélecteur d'actifs
    actifs_disponibles = df["Actif"].tolist()
    actifs_selectionnés = st.multiselect(
        "🗂️ Sélectionne les actifs à afficher :",
        actifs_disponibles,
        default=actifs_disponibles,
    )

    # Filtrage
    df_filtré = df[df["Actif"].isin(actifs_selectionnés)]
    seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 0)
    df_filtré = df_filtré[(df_filtré["% Achat"] >= seuil) | (df_filtré["% Vente"] >= seuil)]

    st.markdown("### 📈 Vue compacte des actifs")

    for _, row in df_filtré.iterrows():
        html = f"""
        <div style="margin-bottom:8px;">
            <strong>{row['Actif']}</strong>
            <div style="width:100%; height:10px; display:flex; background-color:#e0e0e0; border-radius:3px; overflow:hidden; margin:4px 0;">
                <div style="width:{row['% Achat']}%; background-color:#4caf50;"></div>
                <div style="width:{row['% Vente']}%; background-color:#f44336;"></div>
            </div>
            <div style="font-size:12px; color:#555;">
                <span style="color:green;">Achat : {row['% Achat']}%</span>
                &nbsp;&nbsp;&nbsp;
                <span style="color:red;">Vente : {row['% Vente']}%</span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# === Onglet 2 : Rapport COT
elif onglet == "📄 Rapport COT":
    st.subheader("📄 Rapport COT – Commitments of Traders")
    st.info("Cette section sera ajoutée prochainement.")
