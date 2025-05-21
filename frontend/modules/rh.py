import customtkinter as ctk
from backend.logic.rh import obtener_empleados, agregar_empleado, obtener_departamentos, eliminar_empleado, actualizar_empleado

class ModuloRH(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack_propagate(False)
        
        # ---- Pestañas ----
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Pestaña 1: Lista de empleados
        self.tab_lista = self.tabs.add("📋 Lista de Empleados")
        self._crear_lista_empleados()
        
        # Pestaña 2: Registrar nuevo
        self.tab_registro = self.tabs.add("➕ Registrar Empleado")
        self._crear_formulario_registro()

    def _crear_lista_empleados(self):
        # Scrollable Frame
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_lista)
        self.scroll_frame.pack(expand=True, fill="both") 
              
        # Lista inicial
        self._actualizar_lista()

    def _crear_formulario_registro(self):
        form_frame = ctk.CTkFrame(self.tab_registro)
        form_frame.pack(pady=20, padx=30, fill="x")

        departamentos = obtener_departamentos()
        depts = { nombre: id for id, nombre in departamentos }
        
        # Campos del formulario
        campos = [
            ("Nombre", "entry_nombre"),
            ("RFC", "entry_rfc"),
            ("Salario", "entry_salario")
        ]
        
        for i, (label, attr_name) in enumerate(campos):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            setattr(self, attr_name, entry)
        
        # Agrega justo después del último campo del bucle "campos"
        
        ctk.CTkLabel(form_frame, text="Departamento").grid(row=3, column=0, padx=0, pady=5, sticky="e")
        self.combo_dptos = ctk.CTkComboBox(
            master= form_frame,
            values= [nombre for _, nombre in departamentos],
            state = "readonly"
        )
        
        self.combo_dptos.grid(row=len(campos), column=1, padx=5, pady=5, sticky="ew")  
        self.combo_dptos.set("") 

        self.frame_contraseña = ctk.CTkFrame(form_frame)
        self.frame_contraseña.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.frame_contraseña.grid_remove()  
       
        # Botón de registro
        self.btn_registrar = ctk.CTkButton(
            form_frame,
            text="Registrar",
            command=self._registrar_empleado,
            fg_color="#3498db"
        )
        self.btn_registrar.grid(row=5, columnspan=2, pady=15)
        print("Departamentos cargados:", [nombre for _, nombre in departamentos])
        self._restaurar_formulario()

    def _actualizar_lista(self):
        try:
            # Limpiar widgets existentes
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            
            # Obtener datos
            empleados = obtener_empleados()
            print(f"Debug - Empleados obtenidos: {empleados}")  # Para verificar
            
            if not empleados:
                ctk.CTkLabel(
                    self.scroll_frame,
                    text="No hay empleados registrados",
                    font=("Arial", 12)
                ).pack(pady=20)
                return
            
            # Crear encabezados
            headers = ["ID", "Nombre", "RFC", "Salario", "Correo", "Contraseña", "Departamento", "Acciones"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(
                    self.scroll_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    text_color="#3498db"
                ).grid(row=0, column=col, padx=10, pady=5, sticky="ew")
            
            # Mostrar datos
            for row, emp in enumerate(empleados, start=1):
                ctk.CTkLabel(self.scroll_frame, text=str(emp["id"])).grid(row=row, column=0, padx=10)
                ctk.CTkLabel(self.scroll_frame, text=emp["nombre"]).grid(row=row, column=1, padx=10)
                ctk.CTkLabel(self.scroll_frame, text=emp["rfc"]).grid(row=row, column=2, padx=10)
                ctk.CTkLabel(self.scroll_frame, text=f"${emp['salario']:,.2f}").grid(row=row, column=3, padx=10)
                ctk.CTkLabel(self.scroll_frame, text=emp["correo"]).grid(row=row, column=4, padx=10)
                # --- Campo de contraseña con ocultamiento dinámico ---
                clave_visible = ctk.StringVar(value="******")
                clave_real = emp["contraseña"]

                # Label que muestra la contraseña (oculta por defecto)
                label_contra = ctk.CTkLabel(self.scroll_frame, textvariable=clave_visible)
                label_contra.grid(row=row, column=5, padx=10)

                # Función para alternar visibilidad
                def toggle_contra(lbl=label_contra, var=clave_visible, real=clave_real):
                    if var.get() == "******":
                        var.set(real)
                    else:
                        var.set("******")

                # Botón 👁 para mostrar/ocultar
                btn_toggle = ctk.CTkButton(
                    self.scroll_frame,
                    text="👁",
                    width=25,
                    height=20,
                    command=toggle_contra,
                    fg_color="black",       # sin fondo
                    hover_color="Darkgray",    # sin hover
                    text_color="#3498db",         # color del ícono/texto
                    border_width=0,
                    font=("Arial", 14)
                )
                btn_toggle.grid(row=row, column=5, padx=(100, 0))  # coloca el botón a la derecha

                ctk.CTkLabel(self.scroll_frame, text=emp["departamento"]).grid(row=row, column=6, padx=10)
                # --- Botones de acción ---
                frame_accion = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                frame_accion.grid(row=row, column=7, padx=5, pady=2)

                btn_editar = ctk.CTkButton(frame_accion, text="Actualizar", width=32, height=24, command=lambda e=emp: self._editar_empleado(e))
                btn_editar.pack(side="left", padx=2)

                btn_borrar = ctk.CTkButton(frame_accion, text="Eliminar", width=32, height=24, fg_color="#e74c3c",
                                        hover_color="#c0392b", command=lambda e=emp: self._confirmar_eliminar(e["id"]))
                btn_borrar.pack(side="left", padx=2)

                
        except Exception as e:
            print(f"Error en _actualizar_lista: {e}")
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"Error al cargar datos: {str(e)}",
                text_color="red"
            ).pack()

    def _registrar_empleado(self):
        try:
            # 1. Validación de campos
            nombre = self.entry_nombre.get().strip()
            rfc = self.entry_rfc.get().strip()
            salario_text = self.entry_salario.get().strip()
            depto_nombre = self.combo_dptos.get().strip()

            if not all([nombre, rfc, salario_text, depto_nombre]):
                raise ValueError("Todos los campos son obligatorios")

            # 2. Conversión de salario
            try:
                salario = float(salario_text)
                if salario <= 0:
                    raise ValueError("El salario debe ser mayor a 0")
            except ValueError:
                raise ValueError("El salario debe ser un número válido")

            # 3. Obtener ID del departamento
            deptos = { nombre: id for id, nombre in obtener_departamentos()}
            if depto_nombre not in deptos:
                raise ValueError("Seleccione un departamento válido")
            
            depto_id = deptos[depto_nombre]

            # 4. Registrar empleado
            datos = {
                "nombre": nombre,
                "rfc": rfc,
                "salario": salario,
                "depto_id": depto_id
            }

            resultado = agregar_empleado(**datos)
            if not resultado:
                raise RuntimeError("No se pudo registrar el empleado")

            # 5. Feedback y limpieza
            self.mostrar_notificacion("✅ Empleado registrado correctamente")
            self._limpiar_formulario()
            self._actualizar_lista()
            self.tabs.set("📋 Lista de Empleados")

        except ValueError as e:
            self.mostrar_notificacion(f"❌ Error: {str(e)}", error=True)
        except Exception as e:
            self.mostrar_notificacion(f"❌ Error inesperado: {str(e)}", error=True)

    def mostrar_notificacion(self, mensaje, error=False):
        notif = ctk.CTkToplevel(self)
        notif.title("Notificación" if not error else "Error")
        notif.geometry("400x100")
        notif.resizable(False, False)
        
        # Centrar la notificación
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 50
        notif.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(
            notif,
            text=mensaje,
            text_color=("#e74c3c" if error else "#27ae60"),
            font=("Arial", 12)
        ).pack(pady=10)
        
        ctk.CTkButton(
            notif,
            text="Aceptar",
            command=notif.destroy,
            width=100
        ).pack(pady=5)

    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_rfc.delete(0, "end")
        self.entry_salario.delete(0, "end")
        self.combo_dptos.set("")

    def _confirmar_eliminar(self, empleado_id):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Confirmar eliminación")
        ventana.geometry("300x120")

        ctk.CTkLabel(ventana, text="¿Deseas eliminar este empleado?", font=("Arial", 12)).pack(pady=10)
        ctk.CTkButton(ventana, text="Eliminar", fg_color="#e74c3c", command=lambda: self._eliminar(empleado_id, ventana)).pack(pady=5)
        ctk.CTkButton(ventana, text="Cancelar", command=ventana.destroy).pack()

    def _eliminar(self, empleado_id, ventana):
        if eliminar_empleado(empleado_id):
            ventana.destroy()
            self._actualizar_lista()
            self.mostrar_notificacion("✅ Empleado eliminado correctamente")
        else:
            self.mostrar_notificacion("❌ No se pudo eliminar el empleado", error=True)

    def _editar_empleado(self, emp):
        self.tabs.set("➕ Registrar Empleado")
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, emp["nombre"])
        self.entry_rfc.delete(0, "end")
        self.entry_rfc.insert(0, emp["rfc"])
        self.entry_salario.delete(0, "end")
        self.entry_salario.insert(0, str(emp["salario"]))
        self.combo_dptos.set(emp["departamento"])
        for widget in self.frame_contraseña.winfo_children():
            widget.destroy()

        self.frame_contraseña.grid()
        ctk.CTkLabel(self.frame_contraseña, text="Contraseña").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_contraseña = ctk.CTkEntry(self.frame_contraseña, show="*")
        self.entry_contraseña.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_contraseña.insert(0, emp["contraseña"])
        
        self._modo_edicion_id = emp["id"]

        # Cambiar texto del botón
        self.btn_registrar.configure(text="Actualizar", command=self._guardar_edicion)

    def _guardar_edicion(self):
        try:
            nombre = self.entry_nombre.get().strip()
            rfc = self.entry_rfc.get().strip()
            salario = float(self.entry_salario.get().strip())
            depto_nombre = self.combo_dptos.get().strip()
            deptos = {nombre: id for id, nombre in obtener_departamentos()}
            depto_id = deptos[depto_nombre]
            contraseña = self.entry_contraseña.get().strip() if hasattr(self, "entry_contraseña") else None


            if actualizar_empleado(self._modo_edicion_id, nombre, rfc, salario, depto_id, contraseña):
                self.mostrar_notificacion("✅ Empleado actualizado")
                self._restaurar_formulario()
                self._limpiar_formulario()
                self._actualizar_lista()
                self.tabs.set("📋 Lista de Empleados")
            else:
                self.mostrar_notificacion("❌ No se pudo actualizar", error=True)

        except Exception as e:
            self.mostrar_notificacion(f"❌ Error: {e}", error=True) 
    
    def _restaurar_formulario(self):
        if hasattr(self, "_modo_edicion_id"):
            del self._modo_edicion_id
        self.btn_registrar.configure(text="Registrar", command=self._registrar_empleado)
        self._modo_edicion_id = None
        self.entry_nombre.delete(0, "end")
        self.entry_rfc.delete(0, "end")
        self.entry_salario.delete(0, "end")
        if hasattr(self, "entry_contraseña"):
            self.entry_contraseña.delete(0, "end")
        self.combo_dptos.set("")
        self.frame_contraseña.grid_remove()


