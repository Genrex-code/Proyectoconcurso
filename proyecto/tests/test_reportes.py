"""
test_reportes.py
Prueba básica del módulo salida
"""

import pandas as pd
from modules.salida import guardar_resultados
from pathlib import Path


def test_guardar_resultados(tmp_path):

    df = pd.DataFrame({
        "id_cliente": [1, 2],
        "recomendacion": ["demo1", "demo2"]
    })

    config = {
        "output_path": tmp_path
    }

    guardar_resultados(df, config)

    archivos = list(Path(tmp_path).glob("*"))
    assert len(archivos) > 0
