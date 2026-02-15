"""
test_recomendador.py
Prueba básica del recomendador HPE
"""

import pandas as pd
from modules.recomendador import recomendar_hpe


def test_recomendador_basico():

    segmentos = pd.DataFrame({
        "id_cliente": [1, 2, 3],
        "segmento": ["alto", "medio", "bajo"]
    })

    recomendaciones = recomendar_hpe(segmentos)

    assert "recomendacion" in recomendaciones.columns
    assert len(recomendaciones) == 3
