import os
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "backend" / "database.py"

# Configuración de la BD
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Otros ajustes
DEBUG = True