# myfxbook_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# === Lancement du navigateur avec WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# === Accès à la page Myfxbook
print("🔄 Ouverture de Myfxbook...")
driver.get("https://www.myfxbook.com/community/outlook")
time.sleep(5)

# === Pop-up Cookies
try:
    driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]").click()
    print("🍪 Cookies acceptés")
    time.sleep(1)
except:
    print("ℹ️ Aucun popup cookies")

# === Pop-up Redirection
try:
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continue to myfxbook.com')]").click()
    print("➡️ Redirection validée")
    time.sleep(1)
except:
    print("ℹ️ Aucun popup redirection")

# === Pop-up Notifications
try:
    driver.find_element(By.XPATH, "//button[contains(text(), 'Later')]").click()
    print("🔕 Notifications refusées")
    time.sleep(1)
except:
    print("ℹ️ Aucun popup notifications")

# === Attente du chargement
time.sleep(5)

# === Extraction des données à partir des balises fiables
rows = driver.find_elements(By.CSS_SELECTOR, "tr.outlook-symbol-row")
data = []

for row in rows:
    try:
        actif = row.get_attribute("symbolname")
        achat_div = row.find_element(By.CSS_SELECTOR, "div.progress-bar-success")
        vente_div = row.find_element(By.CSS_SELECTOR, "div.progress-bar-danger")

        achat = float(achat_div.get_attribute("style").replace("width:", "").replace("%;", "").strip())
        vente = float(vente_div.get_attribute("style").replace("width:", "").replace("%;", "").strip())

        data.append([actif, achat, vente])
    except:
        continue

# === Fermeture du navigateur
driver.quit()

# === Génération du fichier CSV avec sélection d'actifs
actifs_voulus = [
    "EURUSD", "GBPUSD", "USDJPY", "GBPJPY", "USDCAD", "EURAUD", "EURJPY",
    "AUDCAD", "AUDJPY", "AUDNZD", "AUDUSD", "CADJPY", "EURCAD", "EURCHF",
    "EURGBP", "EURNZD", "GBPCAD", "GBPCHF", "NZDCAD", "NZDJPY", "NZDUSD",
    "USDCHF", "CHFJPY", "AUDCHF", "GBPNZD", "NZDCHF", "XAUUSD", "CADCHF", "GBPAUD"
]

df = pd.DataFrame(data, columns=["Actif", "% Achat", "% Vente"])
df = df[df["Actif"].isin(actifs_voulus)]
df.to_csv("sentiment.csv", index=False)
print(f"✅ sentiment.csv mis à jour avec {len(df)} actifs")
