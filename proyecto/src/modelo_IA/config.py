from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR /"models"
MODEL_DIR.mkdir(exist_ok = True)

Model_NAME = "modelo_HPE.PKL"

RANDOM_STATE = 42
N_ESTIMATORS = 300
MAX_DEPTH = 12
TEST_SIZE = 0.2
