"""
salida.py
Modulo encargado de guardar resultados del sistema IA HPE
"""

from pathlib import Path
import pandas as pd
from datetime import datetime


def log(msg):
    print(f"[Salida] {msg}")


def crear_resumen(df):
    """
    Genera resumen por segmento y prioridad
    """
    resumen_segmentos = df["segmento"].value_counts()
    resumen_prioridad = df["prioridad"].value_counts()

    resumen = pd.DataFrame({
        "segmentos": resumen_segmentos,
        "prioridades": resumen_prioridad
    }).fillna(0)

    return resumen


def guardar_resultados(df, config):
    """
    Guarda resultados del pipeline

    config ejemplo:
    {
        "output_path": "results/",
        "modo": "test"
    }
    """

    base = Path(config["output_path"])
    base.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    archivo_csv = base / f"resultados_{timestamp}.csv"
    archivo_excel = base / f"resultados_{timestamp}.xlsx"
    archivo_resumen = base / f"resumen_{timestamp}.csv"

    # Guardar CSV
    df.to_csv(archivo_csv, index=False)
    log(f"CSV guardado en {archivo_csv}")

    # Guardar Excel
    df.to_excel(archivo_excel, index=False)
    log(f"Excel guardado en {archivo_excel}")

    # Guardar resumen
    resumen = crear_resumen(df)
    resumen.to_csv(archivo_resumen)
    log(f"Resumen guardado en {archivo_resumen}")

    return {
        "csv": archivo_csv,
        "excel": archivo_excel,
        "resumen": archivo_resumen
    }
