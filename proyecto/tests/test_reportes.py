def test_reportes_crea_archivo(tmp_path):
    from src.salida.reportes import guardar_resultados
    import pandas as pd

    df = pd.DataFrame({"a":[1]})
    config = {"output_path": tmp_path}

    guardar_resultados(df,config)

    assert any(tmp_path.iterdir())
    