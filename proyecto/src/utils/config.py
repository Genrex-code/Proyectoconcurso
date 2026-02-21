from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
config = {
    "data_path": BASE_DIR / "data" / "synthetic",
    "output_path": BASE_DIR / "results",
    "modo": "test"
}
