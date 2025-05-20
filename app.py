import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyse de Marché", layout="wide")
st.title("🗭 Tableau de bord marché – Forex & COT")

# === Navigation
onglet = st.sidebar.radio("📂 Choisis une catégorie :", ["📊 Sentiment Forex", "📄 Rapport COT", "📈 Calculateur S&P500"])

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

# === Onglet Sentiment Forex
if onglet == "📊 Sentiment Forex":
    st.subheader("📊 Sentiment Forex – Vue compacte")

    df = charger_donnees()

    # Filtrage par pourcentage
    seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 70)
    df_filtré = df[(df["% Achat"] >= seuil) | (df["% Vente"] >= seuil)]

    # Liste dynamique des actifs filtrés
    actifs_disponibles = df_filtré["Actif"].tolist()
    actifs_selectionnés = st.multiselect(
        "📂 Sélectionne les actifs à afficher :",
        options=actifs_disponibles,
        default=actifs_disponibles,
    )

    # Refiltrage selon sélection manuelle
    df_affichage = df_filtré[df_filtré["Actif"].isin(actifs_selectionnés)]

    st.markdown("### 📈 Actifs avec barres combinées")

    for _, row in df_affichage.iterrows():
        html = f"""
        <div style="margin-bottom:8px;">
            <strong>{row['Actif']}</strong>
            <div style="width:100%; height:10px; display:flex; background-color:#e0e0e0; border-radius:3px; overflow:hidden; margin:4px 0;">
                <div style="width:{row['% Achat']}%; background-color:#2ecc71;"></div>
                <div style="width:{row['% Vente']}%; background-color:#e74c3c;"></div>
            </div>
            <div style="font-size:12px; color:#555;">
                <span style="color:green;">Achat : {row['% Achat']}%</span>
                &nbsp;&nbsp;&nbsp;
                <span style="color:red;">Vente : {row['% Vente']}%</span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# === Onglet COT
elif onglet == "📄 Rapport COT":
    st.subheader("📄 Rapport COT – à venir")
    st.info("Cette section sera ajoutée prochainement.")

# === Onglet Calculateur Google Sheet
elif onglet == "📈 Calculateur S&P500":
    st.subheader("📈 Calculateur S&P500 (Google Sheet)")

    url = "https://docs.google.com/spreadsheets/d/1VNGBo3dYj06noVyK_5miTprbxDKwEbWTCFYPuHGdEfs/pubhtml"
    st.components.v1.iframe(url, height=600, scrolling=True)
