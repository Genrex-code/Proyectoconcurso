from modules.recolector import carga_datos

def test_recolector():
    config = {"data_path": "tests/data"}
    clientes, eventos, historial = carga_datos(config)

    assert len(clientes) == 3
    assert "empresa" in clientes.columns
