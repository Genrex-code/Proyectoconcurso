import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def limpiar_y_validar_features(df, columnas_requeridas):
    """
    Limpia datos nulos, corrige nombres de columnas y maneja outliers.
    """
    # 1. Corregido: .columns en lugar de .columnas
    faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if faltantes:
        logger.warning(f"⚠️ Columnas faltantes: {faltantes}. Rellenando con valores neutros.")
        for col in faltantes:
            df[col] = 0 # O la mediana histórica

    # 2. Manejo de valores extremos (Outliers) para no confundir a la IA
    # Limitamos los valores numéricos entre el percentil 1 y 99
    for col in df.select_dtypes(include=[np.number]).columns:
        limite_superior = df[col].quantile(0.99)
        df[col] = df[col].clip(upper=limite_superior)

    # 3. Limpieza de infinitos y nulos
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return df

def normalizar_score(Y):
    """Escala los resultados al rango 0-100 para visualización de negocio"""
    if len(Y) == 0: return Y
    Y_min, Y_max = Y.min(), Y.max()
    # Evitamos división por cero con 1e-6
    return 100 * (Y - Y_min) / (max(Y_max - Y_min, 1e-6))

def generar_señal_intento(texto_scraping):
    """
    Busca keywords de HPE y devuelve un valor numérico de relevancia.
    """
    keywords = ['cloud', 'hybrid', 'server', 'storage', 'greenlake', 'ai', 'edge']
    count = 0
    if isinstance(texto_scraping, str):
        texto = texto_scraping.lower()
        for word in keywords:
            if word in texto:
                count += 1
    return count