import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse de Marché", layout="wide")
st.title("🗭 Tableau de bord marché – Forex & COT")

# === Navigation
onglet = st.sidebar.radio("📂 Choisis une catégorie :", ["📊 Sentiment Forex", "📄 Rapport COT", "🔗 Corrélations Forex", "🗓️ Calendrier Économique"])

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

# === Onglet Sentiment Forex
if onglet == "📊 Sentiment Forex":
    st.subheader("📊 Sentiment Forex – Vue compacte")

    df = charger_donnees()

    seuil = st.slider("Afficher les actifs avec plus de X% d'achat ou de vente", 0, 100, 70)
    df_filtré = df[(df["% Achat"] >= seuil) | (df["% Vente"] >= seuil)]

    actifs_disponibles = df_filtré["Actif"].tolist()
    actifs_selectionnés = st.multiselect(
        "📂 Sélectionne les actifs à afficher :",
        options=actifs_disponibles,
        default=actifs_disponibles,
    )

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

# === Onglet Rapport COT
elif onglet == "🔗 Corrélations Forex":
    st.subheader("🔗 Corrélation des paires Forex (via fichier CSV)")

    try:
        df_corr = pd.read_csv("correlation_matrix.csv", sep="\t", index_col=0)

        # Remplacer les NaN par 0, arrondir et convertir en entier
        df_clean = df_corr.fillna(0).round(0).astype(int)

        st.markdown("### 📋 Tableau des corrélations (%) avec dégradé de couleur")
        styled = df_clean.style.background_gradient(cmap="RdYlGn", axis=None).format("{:.0f}")
        st.dataframe(styled)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {e}")

# === Onglet Calendrier Économique
elif onglet == "🗓️ Calendrier Économique":
    st.subheader("🗓️ Calendrier Économique – Investing.com")
    st.markdown("""
<iframe src="https://sslecal2.investing.com?ecoDay=week&timezone=56&importance=3&currencies=5,6,7,8,9,10,17,24&columns=exc_currency,importance,event,time,actual,forecast,previous&features=datepicker,timezone,tabs&calType=week&lang=1"
        width="100%" height="600" frameborder="0" allowfullscreen="true" marginwidth="0" marginheight="0" style="border:1px solid #ccc;"></iframe>
""", unsafe_allow_html=True)


