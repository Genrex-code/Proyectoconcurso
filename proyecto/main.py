from modules.recolector import carga_datos

config = {"data_path": "data/synthetic/"}

clientes, eventos, historial = carga_datos(config)

print(clientes.head())
