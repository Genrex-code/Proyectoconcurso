from modules.extractor import extraer_senales
import pandas as pd

def test_extractor():
    clientes = pd.read_csv("tests/data/clientes.csv")
    eventos = pd.read_csv("tests/data/eventos.csv")
    historial = pd.read_csv("tests/data/historial.csv")

    features = extraer_senales(clientes, eventos, historial)

    assert "score_base" in features.columns
