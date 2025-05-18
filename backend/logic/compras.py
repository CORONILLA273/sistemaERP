from backend.database import Session, Proveedor, Compra, DetalleCompra, Producto, MateriaPrima
from datetime import datetime

def registrar_proveedor(nombre: str, contacto: str, telefono: str):
    session = Session()
    try:
        proveedor = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono)
        session.add(proveedor)
        session.commit()
        session.refresh(proveedor)
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al registrar proveedor: {e}")
        return False
    finally:
        session.close()

def obtener_proveedores():
    session = Session()
    try:
        return session.query(Proveedor.id, Proveedor.nombre).all()
    finally:
        session.close()

def registrar_compra(proveedor_id: int, materias: list):
    """
    productos: lista de dicts con 'producto_id', 'cantidad', 'precio_unitario'
    """
    session = Session()
    try:
        total = 0
        detalles = []

        for item in materias:
            materia = session.query(MateriaPrima).get(item['materia_id'])
            if not materia:
                raise ValueError(f"Materia ID {item['materia_id']} no existe")

            precio = item['precio']
            cantidad = item['cantidad']
            subtotal = precio * cantidad
            total += subtotal


            detalles.append(DetalleCompra(
                materia_id=materia.id,
                cantidad=cantidad,
                precio_unitario=precio
            ))

        compra = Compra(
            fecha=datetime.now(),
            proveedor_id=proveedor_id,
            total=total
        )
        session.add(compra)
        session.flush()  # Obtener ID

        for d in detalles:
            d.compra_id = compra.id
            session.add(d)

        session.commit()
        return True

    except Exception as e:
        session.rollback()
        print(f"Error en registrar_compra: {e}")
        return False
    finally:
        session.close()

def obtener_compras():
    session = Session()
    try:
        compras = session.query(Compra).all()
        resultado = []
        for c in compras:
            detalles = session.query(DetalleCompra).filter_by(compra_id=c.id).all()
            materias = [{
                "nombre": d.materia.nombre,
                "cantidad": d.cantidad,
                "precio": d.precio_unitario
            } for d in detalles]

            resultado.append({
                "id": c.id,
                "fecha": c.fecha.strftime("%Y-%m-%d"),
                "proveedor": c.proveedor.nombre,
                "total": c.total,
                "materias": materias
            })
        return resultado
    except Exception as e:
        print(f"Error en obtener_compras: {e}")
        return []
    finally:
        session.close()

def obtener_productos_para_compra():
    session = Session()
    try:
        productos = session.query(Producto).all()
        return [{"id": p.id, "nombre": p.nombre, "precio": p.precio, "stock": p.stock} for p in productos]
    finally:
        session.close()

def obtener_materias_primas():
    session = Session()
    try:
        materias = session.query(MateriaPrima).all()
        return [{"id": m.id, "nombre": m.nombre, "unidad": m.unidad, "precio": m.precio} for m in materias]
    finally:
        session.close()
