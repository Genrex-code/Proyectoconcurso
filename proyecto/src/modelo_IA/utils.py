import numpy as np
import pandas as pd

def validar_features ( df,columnas_requeridas):
    faltantes = [col for col in columnas_requeridas
                 if col not in df.columnas]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    

def normalizar_score(Y):
    Y_min, Y_max = min(Y), max(Y)
    return 100 * (Y - Y_min) / (Y_max - Y_min + 1e-6)


def generar_target_sintetico ( df):
    score = (
        df["ingresos_anuales"] * 0.00001 + 
        df["crecimiento_anual"] *2 +
        df["visitas_web"] *.5 +
        df["compras_previas_monto"]* 0.0001
    )
    ruido = np.random.normal (0,5, len(df))
    return normalizar_score(score + ruido)