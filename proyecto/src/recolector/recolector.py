"""
recolector.py
Modulo encargado de cargar datos desde CSV o Excel
para el sistema IA HPE
"""

from email.mime import base
from pathlib import Path
import pandas as pd


print ("Cargando módulo recolector...")
print ("buscandoen:", base.resolve())

def log(msg):
    print(f"[Recolector] {msg}")


def validar_archivo(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"El archivo {path} no existe.")


def validar_columnas(df, columnas, nombre_tabla):
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        raise ValueError(
            f"Las columnas {faltantes} no existen en la tabla '{nombre_tabla}'"
        )


def leer_archivo(path: Path):
    """Lee CSV o Excel automáticamente"""
    if path.suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    elif path.suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Formato no soportado: {path}")


def limpiar_basico(df):
    """Elimina duplicados y rellena nulos"""
    df = df.drop_duplicates()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("NULO")
        else:
            df[col] = df[col].fillna(0)

    return df


def carga_datos(config):
    """
    Carga clientes, eventos e historial

    config ejemplo:
    {"data_path": "data/synthetic/"}
    """

    base = Path(config["data_path"])

    path_clientes = base / "clientes.csv"
    path_eventos = base / "eventos.csv"
    path_historial = base / "historial.csv"

    # Validar existencia
    validar_archivo(path_clientes)
    validar_archivo(path_eventos)
    validar_archivo(path_historial)

    log("Archivos encontrados")

    # Leer archivos
    clientes = leer_archivo(path_clientes)
    eventos = leer_archivo(path_eventos)
    historial = leer_archivo(path_historial)

    log("Archivos cargados en memoria")

    # Validar columnas mínimas
    validar_columnas(
        clientes,
        ["id_clientes", "nombre", "empresa", "industria"],
        "clientes"
    )

    validar_columnas(
        eventos,
        ["id_cliente", "tipo_evento", "fecha"],
        "eventos"
    )

    validar_columnas(
        historial,
        ["id_cliente", "compras_previas"],
        "historial"
    )

    log("Columnas validadas")

    # Limpieza básica
    clientes = limpiar_basico(clientes)
    eventos = limpiar_basico(eventos)
    historial = limpiar_basico(historial)

    # Convertir fechas si existen
    if "fecha" in eventos.columns:
        eventos["fecha"] = pd.to_datetime(eventos["fecha"], errors="coerce")

    log(f"Clientes cargados: {len(clientes)}")
    log(f"Eventos cargados: {len(eventos)}")
    log(f"Historial cargado: {len(historial)}")

    if clientes.empty:
        raise ValueError("Tabla clientes vacía")

    return clientes, eventos, historial
