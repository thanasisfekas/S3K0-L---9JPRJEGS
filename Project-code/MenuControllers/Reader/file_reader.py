from pathlib import Path

import pandas as pd

class File_reader:
    def __init__(self, file:str) -> None:
        requested_path = Path(file)
        if not requested_path.exists() and not requested_path.is_absolute():
            data_path = Path(__file__).resolve().parents[2] / "Data" / requested_path.name
            if data_path.exists():
                requested_path = data_path

        self.file = str(requested_path)
        self.data = pd.read_csv(self.file)


 
