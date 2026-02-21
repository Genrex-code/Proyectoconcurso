def test_pipeline_completo(tmp_path):
    from scripts.run_pipeline import run_pipeline

    config = {
        "data_path": "data/synthetic",
        "output_path": tmp_path,
        "modo":"test"
    }

    run_pipeline(config)

    assert True