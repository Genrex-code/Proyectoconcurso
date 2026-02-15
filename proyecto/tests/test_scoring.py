from modules.scoring import calcular_score
import pandas as pd

def test_scoring():
    df = pd.DataFrame({
        "score_base":[10,50,90]
    })

    scores = calcular_score(df)

    assert max(scores["score_total"]) <= 100
