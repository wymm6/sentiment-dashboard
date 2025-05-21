from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_calendar_with_browser():
    service = Service("/Users/walidhamdi/Documents/sentiment-dashboard/chromedriver")  # ton chemin local
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ou retire-le pour voir la fenêtre
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    url = "https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=3&features=datepicker,timezone,timeselector,filters&countries=25,6,37,72,22,17,39,35,43,12,4,5&calType=week&timeZone=58&lang=1"
    driver.get(url)

    time.sleep(5)  # attendre que la page charge

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    rows = soup.select("tr.js-event-item")
    events = []
    for row in rows:
        def cell_text(cls):
            cell = row.select_one(cls)
            return cell.get_text(strip=True) if cell else ""

        events.append({
            "datetime": row.get("data-event-datetime", ""),
            "time": cell_text("td.first.left.time"),
            "currency": cell_text("td.left.flagCur.noWrap"),
            "impact": row.select_one("td.sentiment")["title"] if row.select_one("td.sentiment") else "",
            "event": cell_text("td.left.event"),
            "actual": cell_text("td.act"),
            "forecast": cell_text("td.fore"),
            "previous": cell_text("td.prev")
        })

    df = pd.DataFrame(events)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df.to_csv("investing_calendar.csv", index=False)
    print("✅ investing_calendar.csv mis à jour avec Selenium")

if __name__ == "__main__":
    scrape_calendar_with_browser()
