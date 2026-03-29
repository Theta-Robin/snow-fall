from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configuration de Selenium
options = Options()
options.add_argument("--headless")  # Mode sans interface
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# Récupération de la page
driver.get("https://auto.concessionairediamond.fr")
time.sleep(3)  # Attendre le chargement du JS

# Parsing avec BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extraction des véhicules (même logique que précédemment)
vehicles = []
for vehicle in soup.select(".vehicle-item"):
    try:
        title = vehicle.select_one(".vehicle-title").text.strip()
        price = vehicle.select_one(".vehicle-price").text.strip()
        image_url = vehicle.select_one("img.vehicle-image")["src"]
        vehicles.append({"Titre": title, "Prix": price, "Image": image_url})
    except Exception as e:
        print(f"Erreur: {e}")
        continue

# Sauvegarde en CSV
import pandas as pd
df = pd.DataFrame(vehicles)
df.to_csv("vehicules_selenium.csv", index=False, encoding="utf-8-sig")
print("Données sauvegardées avec Selenium.")
