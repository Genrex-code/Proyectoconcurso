import pandas as pd
import numpy as np

def calcular_capa_intencion(df_features):
    """
    Analiza la urgencia y relevancia tecnológica (scraping).
    variables: score_eventos, volumen_noticias
    """
    try:
        # Combinar el peso de los eventos con la cantidad de noticias
        # el volumen de noticias actúa como un multiplicador de confianza
        score_eventos = df_features.get("score_eventos", pd.Series([0])).fillna(0)
        volumen = df_features.get("volumen_noticias", pd.Series([0])).fillna(0)
        score_crudo = score_eventos * (1 + (volumen * 0.1))

        # Limitado a 100 para no romper heurística
        # .applu() → .apply()
        #  min(100, x*10) → min(100, x)
        score_final = score_crudo.apply(lambda x: min(100, x))  # multiplicador sensibilidad
        
        # Salidas
        return score_final.fillna(0.0)
        
    except Exception:
        #Retorna Series alineada con índice
        return pd.Series(0.0, index=df_features.index)
