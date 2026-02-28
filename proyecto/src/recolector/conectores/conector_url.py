import pandas as pd
import requests
from io import StringIO , BytesIO

def cargar(url_dict):
    """
    url_dict: diccionario con las llaves 'clientes' , 'eventos' , 'historial'
    apuntando a sus respectivas URLS de descarga directa.
    """
    dataframes = {}
    headers = {'User-Agent':'Mozilla/5.0 (HPE-analytics-bot)'}

    for nombre,url in url_dict.items():
        print (f"[Conector URL] Peticion a: {url} ...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status() # lanzara error por si la descarga falla 

            if url.endswith('.csv'):
                contenido = StringIO(response.text)
                df = pd.read_csv(contenido)
            else:
                contenido = BytesIO(response.content)
                df = pd.read_excel(contenido)

            dataframes[nombre ] = df
            print (f" {nombre} descargado exitosamente.")

        except Exception as e: 
            raise ConnectionError(f"fallo la descarga de {nombre}: {e}")
        
        return dataframes ["clientes"], dataframes ["eventos"], dataframes ["historial"]
    