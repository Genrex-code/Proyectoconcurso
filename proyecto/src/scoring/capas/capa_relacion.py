import pandas as pd
import numpy as np

def calcular_capa_relacion(df_features):
    """
    Analiza el historial de cliente y su 'humor' actual.
    variables: compras_previas, sentimiento_cliente
    """
    try:
        # Puntos por compras (lealtad)
        puntos_lealtad = df_features.get("compras_previas", pd.Series([0])).fillna(0) * 5

        # Ajuste por sentimiento (hay negativos según el tutorial)
        # y añaden 1 o quitan 1 respectivamente 
        ajuste_sentimiento = df_features.get("sentimiento_cliente", pd.Series([0])).fillna(0) * 20

        score_combinado = puntos_lealtad + ajuste_sentimiento

        # Normalización por mera paranoia
        score_final = score_combinado.apply(lambda x: max(0, min(100, x)))
        return score_final.fillna(20.0)  # se mantiene como un prospecto nuevo sin historial

    except Exception:
        # Retorna Series alineada con índice del DataFrame
        return pd.Series(20.0, index=df_features.index)
