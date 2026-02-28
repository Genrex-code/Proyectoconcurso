from proyecto.src.recolector.recolector_main import carga_datos
from pathlib import Path
import os
from src.utils.my_config import config
# main.py corregido
print("Directorio actual:", os.getcwd())
print("Buscando en:", config["data_path"]) # Debug para estar seguros

# Ahora sí, los archivos se encontrarán solitos
clientes, eventos, historial = carga_datos(config)

print(clientes.head())