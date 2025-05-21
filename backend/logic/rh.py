from backend.database import Session, Empleado, Departamentos
import secrets
import string
import unidecode

def obtener_empleados():
    session = Session()
    try:
        # Consulta directa sin JOIN primero para debug
        print("DEBUG - Todos los empleados (crudo):", session.query(Empleado).all())
        
        # Consulta con JOIN explícito
        empleados = session.query(
            Empleado.id,
            Empleado.nombre,
            Empleado.rfc,
            Empleado.salario,
            Empleado.correo,
            Empleado.contraseña,
            Departamentos.nombre.label('departamento')
        ).join(Departamentos).all()
        
        print("DEBUG - Empleados con join:", empleados)  # Debug adicional
        
        if not empleados:
            # Consulta alternativa sin departamento
            empleados = session.query(Empleado).all()
            return [{
                "id": e.id,
                "nombre": e.nombre,
                "rfc": e.rfc,
                "salario": e.salario,
                "departamento": "No asignado"
            } for e in empleados]
            
        return [dict(e._asdict()) for e in empleados]
        
    except Exception as e:
        print(f"ERROR en obtener_empleados: {str(e)}")
        return []
    finally:
        session.close()

def agregar_empleado(nombre: str, rfc: str, salario: float, depto_id: int):
    session = Session()
    try:
        if not session.query(Departamentos).get(depto_id):
            raise  ValueError("Departamento Inexistente")
        nombre_simple = unidecode.unidecode(nombre.lower().replace(" ", "."))
        correo = f"{nombre_simple}@bnj.com"
         # Contraseña aleatoria de 8 caracteres
        alfabeto = string.ascii_letters + string.digits
        contraseña = ''.join(secrets.choice(alfabeto) for _ in range(8))

        empleado = Empleado(
            nombre = nombre,
            rfc = rfc, 
            salario = salario,
            departamento_id = depto_id,
            correo=correo,
            contraseña=contraseña
        )
        session.add(empleado)
        session.commit()
        session.refresh(empleado)
        print(f"DEBUG - Empleado creado con ID: {empleado.id}")
        return True

    except Exception as e:
        session.rollback()
        print(f"ERROR en agregar_empleado: {str(e)}")
        return False
    finally:
        session.close()

def eliminar_empleado(empleado_id: int):
    session = Session()
    try:
        empleado = session.query(Empleado).get(empleado_id)
        if not empleado:
            raise ValueError("Empleado no encontrado")
        session.delete(empleado)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"ERROR al eliminar empleado: {e}")
        return False
    finally:
        session.close()

def actualizar_empleado(empleado_id: int, nombre: str, rfc: str, salario: float, depto_id: int, contraseña: str):
    session = Session()
    try:
        empleado = session.query(Empleado).get(empleado_id)
        if not empleado:
            raise ValueError("Empleado no encontrado")

        empleado.nombre = nombre
        empleado.rfc = rfc
        empleado.salario = salario
        empleado.departamento_id = depto_id
        empleado.contraseña = contraseña
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"ERROR al actualizar empleado: {e}")
        return False
    finally:
        session.close()

    
def listar_empleados():
    with Session() as session:
        return session.query(Empleado).all()

def obtener_departamentos():
    # Obtiene todos los departamentos como lista de (id, nombre)
    session = Session()
    try: 
        return session.query(Departamentos.id, Departamentos.nombre).all()
    finally:
        session.close()