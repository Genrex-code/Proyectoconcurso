import requests
from bs4 import beautifulsoup
import pandas as pd

def cargar (urls_empresas):
    """
    urls_empresas: lista de diccionarios [{'id_cliente':1,'url': '...'},...]
    """

#palabras clave pero en ingles para que se escuche cihngon

    keywords_hpe = {
        'infra_score': ['data center', 'servidor', 'almacenamiento', 'rack', 'alletra', 'proliant'],
        'growth_score': ['adquisición', 'expansión', 'nueva sede', 'crecimiento', 'inversión'],
        'cloud_score': ['hybrid cloud', 'nube híbrida', 'greenlake', 'saas', 'paas']
    }

    registros_eventos = []

    for item in urls_empresas:
        target = item['url']
        client_id = item['id_cliente']
        print(f"[Scraper] Analizando {target} para cliente {client_id}...")
        
        try:
            res = requests.get(target, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            # Limpiamos el texto para evitar ruido de scripts/estilos
            for script in soup(["script", "style"]):
                script.decompose()
            
            texto = soup.get_text().lower()
            
            # Generar "eventos virtuales" basados en hallazgos
            for categoria, palabras in keywords_hpe.items():
                for p in palabras:
                    if p in texto:
                        registros_eventos.append({
                            'id_cliente': client_id,
                            'tipo_evento': f"mencion_{categoria}",
                            'fecha': pd.Timestamp.now().strftime('%Y-%m-%d'),
                            'detalle': f"Hallazgo de keyword: {p}"
                        })
        except Exception as e:
                        print(f"Salto de URL {target} por error: {e}")
                        # el scraper genera principalmente la tabla de EVENTOS
                        df_eventos = pd.DataFrame(registros_eventos)
                        return df_eventos             