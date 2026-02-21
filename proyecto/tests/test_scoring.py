def test_scoring_no_negativo():
    import pandas as pd
    from src.scoring.scoring import calcular_score

    features = pd.DataFrame({
        "score_eventos":[10],
        "compras_previas":[2]
    })

    scores = calcular_score(features)

    assert scores.iloc[0]["score_total"] >= 0