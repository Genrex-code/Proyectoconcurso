import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO, BytesIO

class RecolectorInteligente:
    def __init__(self, config):
        self.config = config

    def obtener_desde_url(self, url):
        """Descarga CSV/Excel desde una URL directa"""
        print(f"[Recolector] Descargando desde URL: {url}")
        resp = requests.get(url)
        if url.endswith('.csv'):
            return pd.read_csv(StringIO(resp.text))
        else:
            return pd.read_excel(BytesIO(resp.content))

    def scrapear_noticias(self, url_empresa):
        """Busca señales de crecimiento en el sitio web"""
        print(f"[Recolector] Scrapeando señales en: {url_empresa}")
        try:
            # Esto es un scraping básico, luego lo evolucionamos
            html = requests.get(url_empresa, timeout=5).text
            soup = BeautifulSoup(html, 'html.parser')
            texto = soup.get_text().lower()
            
            # Buscamos 'señales' rápidas para el Extractor
            hits = sum(1 for word in ['expansión', 'inversión', 'contratando', 'hpe'] if word in texto)
            return hits
        except:
            return 0

    def ejecutar(self):
        # Aquí decidimos qué motor usar según la config
        if self.config.get("input_type") == "url":
            return self.obtener_desde_url(self.config["source"])
        # ... resto de la lógica