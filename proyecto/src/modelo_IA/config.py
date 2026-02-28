from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_NAME = "modelo_HPE_incremental.pkl" # Cambiamos extensión a minúsculas por estándar
RANDOM_STATE = 42
LEARNING_RATE = 0.01