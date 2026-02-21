from src.recolector.recolector import carga_datos
from pathlib import Path
import os
from src.utils.my_config import config
print("Directorio actual:", os.getcwd())
config = {"data_path": "data/synthetic/"}

clientes, eventos, historial = carga_datos(config)

print(clientes.head())
