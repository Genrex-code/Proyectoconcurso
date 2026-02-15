"""
test_modelo.py
Prueba básica de scoring + clasificador
"""

import pandas as pd
from modules.scoring import calcular_score
from modules.clasificador import clasificar_clientes


def test_modelo_basico():

    # dataset mínimo
    features = pd.DataFrame({
        "id_cliente": [1, 2, 3],
        "score_base": [10, 60, 90]
    })

    scores = calcular_score(features)

    assert "score_total" in scores.columns
    assert scores["score_total"].max() <= 100

    segmentos = clasificar_clientes(scores)

    assert "segmento" in segmentos.columns
    assert len(segmentos) == 3
