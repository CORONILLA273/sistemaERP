from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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
    departamento = relationship("Departamentos")
    activo = Column(Boolean, default=True)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    rfc = Column(String(20))
    direccion = Column(String(200))
    telefono = Column(String(20))

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

class Venta(Base):
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, default=datetime.now())
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    vendedor_id = Column(Integer, ForeignKey('empleados.id'))
    total = Column(Float)
    cliente = relationship("Cliente")
    vendedor = relationship("Empleado")

class DetalleVenta(Base):
    __tablename__ = 'detalles_venta'
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('ventas.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    producto = relationship("Producto")

class Proveedor(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100))
    telefono = Column(String(20))

class Compra(Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, default=datetime.now())
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))
    total = Column(Float)
    proveedor = relationship("Proveedor")

class DetalleCompra(Base):
    __tablename__ = 'detalles_compra'
    id = Column(Integer, primary_key=True)
    compra_id = Column(Integer, ForeignKey('compras.id'))
    materia_id = Column(Integer, ForeignKey('materias_primas.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    materia = relationship("MateriaPrima")

class MateriaPrima(Base):
    __tablename__ = 'materias_primas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    unidad = Column(String(20))  # Ej: "kg", "pzas", "litros"
    precio = Column(Float, nullable=False)


# Crear tablas
def init_db():
    Base.metadata.create_all(engine)
    print("✅ Base de Datos Inicializada")

if __name__ == "__main__":
    init_db()

    # Insertar departamentos básicos
    session = Session()
    try:
        if not session.query(Departamentos).first():
            session.add_all([
                Departamentos(nombre="Dirección"),
                Departamentos(nombre="Contabilidad"),
                Departamentos(nombre="Ventas"),
                Departamentos(nombre="Producción"),
                Departamentos(nombre="Recursos Humanos"),
            ])
        if not session.query(MateriaPrima).first():
            session.add_all([
                MateriaPrima(nombre="Motor eléctrico 1HP", unidad="pieza", precio=1200),
                MateriaPrima(nombre="Impulsor de acero inoxidable", unidad="pieza", precio=350),
                MateriaPrima(nombre="Carcasa de aluminio", unidad="pieza", precio=420),
                MateriaPrima(nombre="Eje de acero templado", unidad="pieza", precio=180),
                MateriaPrima(nombre="Empaques y sellos", unidad="set", precio=95),
                MateriaPrima(nombre="Tornillos y sujetadores inox", unidad="kg", precio=60),
                MateriaPrima(nombre="Rodamientos industriales", unidad="pieza", precio=140),
                MateriaPrima(nombre="Pintura industrial anticorrosiva", unidad="litro", precio=75),
            ])
            session.commit()
    finally:
        session.close()