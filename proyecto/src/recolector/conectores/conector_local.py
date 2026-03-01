import pandas as pd 
from pathlib import Path
from src.utils.my_config import config

def cargar(config):
    """
    CARGA ROBUSTA DESDE ARCHIVOS LOCALES CSV O EXCEL 
    PREVIAMENTE LIMPIADOS
    """
    base = Path("data_path")
    archivos = {
        "clientes": base / "clientes.csv",
        "eventos" : base / "eventos.csv",
        "historial" : base / "historial.csv"
    }

    dataframes = {}

    for nombre, ruta in archivos.items():
        if not ruta.exists():
            #buscar ruta .xlsx si no hay .cvs o excel poes
            ruta_alt = ruta.with_suffix('xlsx')
            if ruta_alt.exists():
                ruta = ruta_alt
            else:
                raise FileNotFoundError(F"Error critico: falta archivo esencial '{nombre}' en {base}") 
            print(f"[Conector Local] Leyendo {nombre} desde {ruta.name}...")


            if ruta.suffix == ".csv":
                df = pd.read_csv (ruta,low_memory = False,encoding='utf-8')
            else:
                df = pd.read_excel(ruta)


                #limpeiza de espacios en nombrs de columnas
            df.columns = df.columns.str.strip()
            dataframes[nombre] = df
            return dataframes ["clientes"], dataframes["eventos"],dataframes["historial"]