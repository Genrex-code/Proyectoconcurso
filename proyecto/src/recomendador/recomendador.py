#se debe ampliar horizontalmente con nuevas señales, pero se deja esta base para el concurso
#recomendable añadir un ranking de productos para cada segmento, pero por ahora a comer :D
#nota: que chingue a su madre el america 
"""
recomendador.py
Modulo que genera recomendaciones comerciales
Sistema IA HPE
"""

import pandas as pd


def elegir_producto(segmento, industria=None):
    """Reglas simples de recomendación"""
    
    if segmento == "Caliente":
        return "Servidor HPE ProLiant"
    
    if segmento == "Tibio":
        return "Almacenamiento HPE Alletra"
    
    return "Newsletter de soluciones HPE"


def elegir_canal(segmento):
    """Canal de contacto"""
    
    if segmento == "Caliente":
        return "Llamada directa"
    
    if segmento == "Tibio":
        return "Email personalizado"
    
    return "Email masivo"


def prioridad(segmento):
    """Nivel de urgencia"""
    
    if segmento == "Caliente":
        return "Alta"
    
    if segmento == "Tibio":
        return "Media"
    
    return "Baja"


def recomendar_hpe(segmentos_df):
    """
    segmentos_df columnas:
    id_cliente | score | segmento
    """

    df = segmentos_df.copy()

    df["producto"] = df["segmento"].apply(elegir_producto)
    df["canal"] = df["segmento"].apply(elegir_canal)
    df["prioridad"] = df["segmento"].apply(prioridad)

    print("Recomendaciones generadas:", len(df))
    print(df["prioridad"].value_counts())

    return df
