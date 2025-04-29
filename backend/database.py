from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# --- MODELOS ---
class Departamentos(Base): 
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True)

class Empleado(Base): 
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    rfc = Column(String(20), unique=True)
    salario = Column(Float)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    activo = Column(Boolean, default=True)

# Crear tablas
def init_db():
    Base.metadata.create_all(engine)
    print("✅ Base de Datos Inicializada")

if __name__ == "__main__":
    init_db()