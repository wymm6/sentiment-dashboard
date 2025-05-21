# corr_matrix_scraper_playwright.py

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# === URL de la matrice de corrélation ===
URL = "https://www.mataf.net/fr/tools/01-01-correlation"

# === Lancement de Playwright (mode non headless pour contourner Cloudflare) ===
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 300, "height": 200})


    print("🔄 Ouverture de la page...")
    page.goto(URL)

    # Attendre que le tableau soit visible
    page.wait_for_selector("tr[data-inst1]", timeout=20000)
    print("✅ Matrice détectée")

    # Récupérer le contenu HTML complet
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    browser.close()

# === Extraction de la matrice ===
data = {}
all_rows = soup.select("tr[data-inst1]")

for row in all_rows:
    ligne = row.get("data-inst1")
    cells = row.select("td[data-inst2]")
    data[ligne] = {}
    for cell in cells:
        colonne = cell.get("data-inst2")
        texte = cell.text.strip()
        try:
            data[ligne][colonne] = float(texte)
        except:
            data[ligne][colonne] = None

# === Construction et sauvegarde ===
df = pd.DataFrame.from_dict(data, orient="index")
df = df.reindex(sorted(df.columns), axis=1)
df.fillna(0).round(0).astype(int).to_csv("correlation_matrix.csv", sep="\t")
print("✅ correlation_matrix.csv généré avec Playwright")
