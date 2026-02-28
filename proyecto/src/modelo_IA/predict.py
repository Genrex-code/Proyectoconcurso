import joblib 
import pandas as pd 
from .config import MODEL_DIR, Model_NAME

def cargar_modelo():
    return joblib.load(MODEL_DIR / MODEL_DIR)


def predecir(df_features):
    modelo = cargar_modelo()
    predicciones = modelo.predect(df_features)
    return predicciones

