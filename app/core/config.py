from pathlib import Path

class Settings:
    # Rutas absolutas
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

    # Nombres de los archivos
    COSTOS_FILE = DATA_DIR / "costos final_1.csv"
    TASAS_FILE = DATA_DIR / "transferencia final_final.csv"
    PD_FILE = DATA_DIR / "pd final_final_2.csv"

settings = Settings()