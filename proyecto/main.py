from src.recolector.recolector import carga_datos
import os
print("Directorio actual:", os.getcwd())
config = {"data_path": "data/synthetic/"}

clientes, eventos, historial = carga_datos(config)

print(clientes.head())
