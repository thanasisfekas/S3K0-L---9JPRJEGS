from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "Data"


def data_path(filename: str) -> Path:
    return DATA_DIR / filename
