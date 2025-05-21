#!/bin/bash

cd ~/Documents/sentiment-dashboard || exit 1

echo "▶️ Lancement des scripts de scraping..."
python3 corr_matrix_scraper_playwright.py && python3 myfxbook_scraper.py

echo "✅ Scripts terminés. Passage au commit Git..."

git add .
git commit -m "🔁 Mis à jour"
git push -f origin main

echo "🚀 Push terminé."

