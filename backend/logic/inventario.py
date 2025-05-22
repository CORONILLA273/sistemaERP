from backend.database import Session, Producto

def agregar_producto(nombre: str, precio: float, stock: int):
    session = Session()
    try:
        producto = Producto(nombre=nombre, precio=precio, stock=stock)
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al agregar producto: {e}")
        return False
    finally:
        session.close()

def obtener_productos():
    session = Session()
    try:
        productos = session.query(Producto).all()
        return [{
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": p.stock
        } for p in productos]
    finally:
        session.close()

def actualizar_producto(producto_id: int, nombre: str, precio: float, stock: int):
    session = Session()
    try:
        producto = session.query(Producto).get(producto_id)
        if not producto:
            return False
        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al actualizar producto: {e}")
        return False
    finally:
        session.close()

def eliminar_producto(producto_id: int):
    session = Session()
    try:
        producto = session.query(Producto).get(producto_id)
        if not producto:
            return False
        session.delete(producto)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        session.close()

