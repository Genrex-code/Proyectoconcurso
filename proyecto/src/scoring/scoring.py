"""
scoring.py
Calcula score de clientes para sistema IA HPE
"""

import pandas as pd


def puntaje_interes(valor):
    tabla = {
        "Alto": 20,
        "Medio": 10,
        "Bajo": 3,
        "Nulo": 0
    }
    return tabla.get(valor, 0)


def puntaje_tamano(valor):
    tabla = {
        "Grande": 15,
        "Mediana": 8,
        "Pequeña": 3
    }
    return tabla.get(valor, 0)


def calcular_score(features):
    """
    features = dataframe del extractor
    retorna dataframe con score
    """

    df = features.copy()

    df["score"] = (
        df["eventos_positivos"] * 10
        - df["eventos_negativos"] * 15
        + df["compras_previas"] * 5
        + df["interes_producto"].apply(puntaje_interes)
        + df["T_empresa"].apply(puntaje_tamano)
    )

    # evitar negativos
    df["score"] = df["score"].clip(lower=0)

    print("Score calculado para", len(df), "clientes")

    return df[["id_cliente", "score"]]
