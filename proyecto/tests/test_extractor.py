def test_extractor_crea_features():
    import pandas as pd
    from src.extractor.extractor import extraer_senales

    clientes = pd.DataFrame({"id_clientes":[1]})
    eventos = pd.DataFrame({"id_cliente":[1], "tipo_evento":["expansion"]})
    historial = pd.DataFrame({"id_cliente":[1], "compras_previas":[2]})

    features = extraer_senales(clientes,eventos,historial)

    assert "score_eventos" in features.columns
    