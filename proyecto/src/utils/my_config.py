from pathlib import Path
#correccion fix de carpetas base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
config = {
    "data_path": BASE_DIR / "data" / "synthetic",
    "output_path": BASE_DIR / "results",
    "modo": "test"
}
