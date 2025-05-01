import os
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "backend" / "database.db"

# Configuración de la BD
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Otros ajustes
DEBUG = True