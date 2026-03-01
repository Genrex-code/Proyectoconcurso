import pandas as pd 
from pathlib import Path
from src.utils.my_config import config

def cargar(config_dict):
    """
    CARGA ROBUSTA DESDE ARCHIVOS LOCALES CSV O EXCEL 
    """
    # 1. Extraemos la ruta real del diccionario (sin comillas en la variable)
    ruta_recibida = config_dict.get("data_path")
    
    if not ruta_recibida:
        raise ValueError("No se proporcionó 'data_path' en la configuración.")
        
    base = Path(ruta_recibida) 
    
    # 2. Definimos los nombres de archivos que buscamos
    archivos_buscados = ["clientes", "eventos", "historial"]
    dataframes = {}

    for nombre in archivos_buscados:
        # Intentamos primero con .csv
        ruta = base / f"{nombre}.csv"
        
        if not ruta.exists():
            # Si no hay .csv, intentamos con .xlsx (con el punto correcto)
            ruta = base / f"{nombre}.xlsx"
            
        if not ruta.exists():
            raise FileNotFoundError(f"Error crítico: No se encontró '{nombre}' (.csv o .xlsx) en {base}") 
        
        print(f"[Conector Local] Leyendo {nombre} desde {ruta.name}...")

        # 3. Lectura según la extensión detectada
        if ruta.suffix == ".csv":
            df = pd.read_csv(ruta, low_memory=False, encoding='utf-8')
        else:
            df = pd.read_excel(ruta)

        # Limpieza rápida: quitar espacios en nombres de columnas
        df.columns = df.columns.str.strip()
        dataframes[nombre] = df

    # 4. Retornamos el diccionario completo para que recolector_main lo maneje
    return dataframes