import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Sentiment Myfxbook", layout="wide")
st.title("📊 Sentiment Forex – Style Myfxbook")

@st.cache_data
def charger_donnees():
    return pd.read_csv("sentiment.csv")

df = charger_donnees()

# Slider de filtrage
seuil = st.slider("Afficher les actifs avec + de X% d'achat ou de vente", 0, 100, 0)
df = df[(df["% Achat"] >= seuil) | (df["% Vente"] >= seuil)]

# Trier les actifs par achat décroissant pour le visuel
df = df.sort_values(by="% Achat", ascending=True)

# Création du graphique style Myfxbook
fig = go.Figure()

fig.add_trace(go.Bar(
    y=df["Actif"],
    x=df["% Achat"],
    name="Achat",
    orientation='h',
    marker=dict(color='green'),
    hovertemplate="% Achat: %{x:.1f}%<extra></extra>"
))

fig.add_trace(go.Bar(
    y=df["Actif"],
    x=[-x for x in df["% Vente"]],
    name="Vente",
    orientation='h',
    marker=dict(color='red'),
    hovertemplate="% Vente: %{x:.1f}%<extra></extra>"
))

fig.update_layout(
    barmode='relative',
    title="💹 Sentiment des traders particuliers par actif",
    xaxis=dict(
        title="Pourcentage",
        tickvals=[-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100],
        ticktext=["100% Vente", "80%", "60%", "40%", "20%", "0", "20%", "40%", "60%", "80%", "100% Achat"],
        range=[-100, 100],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(title="Actif"),
    bargap=0.2,
    height=40 * len(df) + 100,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
