import joblib
import pandas as pd
from src.modelo_IA.config import MODEL_DIR, MODEL_NAME

def predecir(df_features):
    """Predicción con validación de consistencia"""
    path = MODEL_DIR / MODEL_NAME
    if not path.exists():
        raise FileNotFoundError("El cerebro de la IA está vacío. Ejecuta el entrenamiento primero.")
    
    meta = joblib.load(path)
    pipeline = meta['pipeline']
    
    # Reordenar columnas automáticamente para que coincidan con el entrenamiento
    # Esto evita el error de "las columnas están en otro orden"
    df_features = df_features.reindex(columns=meta['features'], fill_value=0)
    
    # Ejecutar predicción
    scores_predichos = pipeline.predict(df_features)
    
    # Razonamiento de salida: Asegurar que el score esté en rango 0-100
    scores_finales = [max(0, min(100, s)) for s in scores_predichos]
    
    return scores_finales