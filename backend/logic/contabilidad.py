# backend/logic/contabilidad.py

from backend.database import Session, Venta, Compra
from sqlalchemy import func

def obtener_ingresos():
    session = Session()
    try:
        ingresos = session.query(
            func.strftime('%Y-%m-%d', Venta.fecha).label("fecha"),
            func.sum(Venta.total).label("total")
        ).group_by("fecha").all()

        return [{"fecha": row.fecha, "total": row.total} for row in ingresos]
    finally:
        session.close()

def obtener_egresos():
    session = Session()
    try:
        egresos = session.query(
            func.strftime('%Y-%m-%d', Compra.fecha).label("fecha"),
            func.sum(Compra.total).label("total")
        ).group_by("fecha").all()

        return [{"fecha": row.fecha, "total": row.total} for row in egresos]
    finally:
        session.close()
