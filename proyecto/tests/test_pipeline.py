"""
test_pipeline_completo.py
Prueba de integración completa
"""

from run_pipeline import run_pipeline


def test_pipeline():

    config = {
        "data_path": "tests/data",
        "output_path": "tests/output",
        "modo": "test"
    }

    run_pipeline(config)
