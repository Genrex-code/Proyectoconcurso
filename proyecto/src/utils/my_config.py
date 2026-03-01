"""
Configuración Global del Sistema HPE AI-Sales Enhancer
Este archivo centraliza los parámetros de negocio y técnicos.
"""
from pathlib import Path
import os

# Detecta la raíz del proyecto (donde está este archivo)
BASE_DIR = Path(__file__).resolve().parents[2]

config = {
    # Ruta a la carpeta de datos sintéticos
    "data_path": BASE_DIR / "data" / "synthetic",
    "output_path": BASE_DIR / "results",
    "modo": "test"
}
# --- 1. CONFIGURACIÓN DE PESOS DEL SCORING (30/40/30) ---
# Permite ajustar la importancia de cada capa heurística
PESOS_SCORING = {
    "valor": 0.30,      # Capacidad económica (ingresos)
    "intencion": 0.40,   # Momentum de mercado (scraping/noticias)
    "relacion": 0.30     # Fidelidad (historial/sentimiento)
}

# --- 2. UMBRALES DE NEGOCIO (Thresholds) ---
# Define los puntos de corte para la toma de decisiones
UMBRALES = {
    "segmento_enterprise": 60,  # Score de valor mínimo para ser Enterprise
    "intencion_alta": 75,       # Score de intención para activar triggers de IA
    "prioridad_critica": 85,     # Score final para marcar como "Llamar Ahora"
    "relacion_riesgo": 35       # Score de relación bajo que activa oferta GreenLake
}

# --- 3. CONFIGURACIÓN DE IA ---
# Parámetros para el entrenamiento incremental
IA_CONFIG = {
    "learning_rate": 0.01,
    "modelo_path": "models/hpe_predictor_v1.pkl",
    "batch_size": 32
}

# --- 4. PARÁMETROS DE SCRAPING / EXTRACTOR ---
# Keywords clave que el becario identificó en el PDF para el mapping
KEYWORDS_HPE = [
    "cloud", "hybrid", "storage", "ai", "ml", "gpu", 
    "server", "networking", "edge", "greenlake", "synergy"
]

# --- 5. LOGGING ---
LOG_LEVEL = "INFO"