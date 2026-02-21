def test_recolector_basico(tmp_path):
    import pandas as pd
    from src.recolector.recolector import carga_datos

    base = tmp_path

    clientes = pd.DataFrame({
        "id_clientes":[1],
        "nombre":["Ana"],
        "empresa":["X"],
        "industria":["Tech"]
    })
    eventos = pd.DataFrame({
        "id_cliente":[1],
        "tipo_evento":["expansion"],
        "fecha":["2024-01-01"]
    })
    historial = pd.DataFrame({
        "id_cliente":[1],
        "compras_previas":[2]
    })

    clientes.to_csv(base/"clientes.csv", index=False)
    eventos.to_csv(base/"eventos.csv", index=False)
    historial.to_csv(base/"historial.csv", index=False)

    config = {"data_path": base}

    c,e,h = carga_datos(config)

    assert len(c) == 1
    assert len(e) == 1
    assert len(h) == 1