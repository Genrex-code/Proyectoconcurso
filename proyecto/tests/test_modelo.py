def test_clasificador_segmentos():
    import pandas as pd
    from src.clasificador.modelo import clasificar_clientes

    scores = pd.DataFrame({"score_total":[90,50,10]})

    seg = clasificar_clientes(scores)

    assert len(seg) == 3