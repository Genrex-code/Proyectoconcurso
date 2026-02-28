import numpy as np
import pandas as pd

def validar_features(df, columnas_requeridas):
    # CORREGIDO: era .columns, no .columnas
    faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

def normalizar_score(Y):
    Y_min, Y_max = Y.min(), Y.max()
    return 100 * (Y - Y_min) / (Y_max - Y_min + 1e-6)