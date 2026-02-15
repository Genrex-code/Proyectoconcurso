"""
generador_speech.py
Modulo que convierte recomendaciones en mensajes legibles
Sistema IA HPE
"""

import pandas as pd


def crear_mensaje(row):
    """
    Genera mensaje para un cliente
    """

    return (
        f"Cliente {row['id_cliente']} clasificado como {row['segmento']} "
        f"con prioridad {row['prioridad']}. "
        f"Recomendar producto: {row['producto']} "
        f"mediante canal: {row['canal']}."
    )


def generar_speech(recomendaciones_df):
    """
    recomendaciones_df columnas:
    id_cliente | segmento | producto | canal | prioridad
    """

    df = recomendaciones_df.copy()

    df["mensaje"] = df.apply(crear_mensaje, axis=1)

    print("Mensajes generados:", len(df))

    return df
