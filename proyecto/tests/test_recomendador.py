def test_recomendador_genera_algo():
    import pandas as pd
    from src.recomendador.recomendador import recomendar_hpe

    seg = pd.DataFrame({"segmento":["alto","medio","bajo"]})

    rec = recomendar_hpe(seg)

    assert len(rec) == 3