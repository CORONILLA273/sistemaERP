# backend/logic/ventas.py

from backend.database import Session, Venta, DetalleVenta, Producto, Cliente, Empleado
from datetime import datetime

def registrar_venta(cliente_id: int, vendedor_id: int, productos: list):
    """
    Registra una venta nueva.

    productos: lista de diccionarios con 'producto_id' y 'cantidad'
    """
    session = Session()
    try:
        total = 0
        detalles = []

        for item in productos:
            producto = session.query(Producto).get(item['producto_id'])
            if not producto:
                raise ValueError(f"Producto ID {item['producto_id']} no existe")
            if producto.stock < item['cantidad']:
                raise ValueError(f"Stock insuficiente para {producto.nombre}")

            precio_unitario = producto.precio
            subtotal = precio_unitario * item['cantidad']
            total += subtotal

            producto.stock -= item['cantidad']  # Descontar del stock

            detalles.append(DetalleVenta(
                producto_id=producto.id,
                cantidad=item['cantidad'],
                precio_unitario=precio_unitario
            ))

        venta = Venta(
            fecha=datetime.now(),
            cliente_id=cliente_id,
            vendedor_id=vendedor_id,
            total=total
        )
        session.add(venta)
        session.flush()  # Obtener el ID de la venta

        for detalle in detalles:
            detalle.venta_id = venta.id
            session.add(detalle)

        session.commit()
        return True

    except Exception as e:
        session.rollback()
        print(f"ERROR en registrar_venta: {str(e)}")
        return False
    finally:
        session.close()

def obtener_ventas():
    """Devuelve una lista de ventas con cliente, vendedor y total."""
    session = Session()
    try:
        ventas = session.query(Venta).all()
        resultado = []
        for venta in ventas:
            detalles = session.query(DetalleVenta).filter_by(venta_id=venta.id).all()
            productos = [{
                "nombre": d.producto.nombre,
                "cantidad": d.cantidad,
                "precio_unitario": d.precio_unitario
            } for d in detalles]

            resultado.append({
                "id": venta.id,
                "fecha": venta.fecha.strftime("%Y-%m-%d"),
                "cliente": venta.cliente.nombre,
                "vendedor": venta.vendedor.nombre,
                "total": venta.total,
                "productos": productos
            })
        return resultado
    except Exception as e:
        print(f"ERROR en obtener_ventas: {str(e)}")
        return []
    finally:
        session.close()

def obtener_productos_disponibles():
    session = Session()
    try:
        productos = session.query(Producto).filter(Producto.stock > 0).all()
        return [{"id": p.id, "nombre": p.nombre, "precio": p.precio, "stock": p.stock} for p in productos]
    finally:
        session.close()

def obtener_clientes():
    session = Session()
    try:
        return session.query(Cliente.id, Cliente.nombre).all()
    finally:
        session.close()

def obtener_vendedores():
    session = Session()
    try:
        return session.query(Empleado.id, Empleado.nombre).all()
    finally:
        session.close()

def obtener_o_crear_cliente_por_nombre(nombre: str):
    session = Session()
    try:
        cliente = session.query(Cliente).filter(Cliente.nombre == nombre).first()
        if cliente:
            return cliente.id
        nuevo = Cliente(nombre=nombre, rfc="", direccion="", telefono="")
        session.add(nuevo)
        session.commit()
        return nuevo.id
    except Exception as e:
        session.rollback()
        print(f"Error en obtener_o_crear_cliente_por_nombre: {e}")
        return None
    finally:
        session.close()
