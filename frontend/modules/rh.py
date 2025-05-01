import customtkinter as ctk
from backend.logic.rh import obtener_empleados, agregar_empleado

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
        
        # Botón de actualización
        btn_actualizar = ctk.CTkButton(
            self.tab_lista,
            text="🔄 Actualizar",
            command=self._actualizar_lista,
            fg_color="#2ecc71"
        )
        btn_actualizar.pack(pady=5)
        
        # Lista inicial
        self._actualizar_lista()

    def _crear_formulario_registro(self):
        form_frame = ctk.CTkFrame(self.tab_registro)
        form_frame.pack(pady=20, padx=30, fill="x")
        
        # Campos del formulario
        campos = [
            ("Nombre", "entry_nombre"),
            ("RFC", "entry_rfc"),
            ("Salario", "entry_salario"),
            ("Departamento ID", "entry_depto")
        ]
        
        for i, (label, attr_name) in enumerate(campos):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            setattr(self, attr_name, entry)
        
        # Botón de registro
        btn_registrar = ctk.CTkButton(
            form_frame,
            text="Registrar",
            command=self._registrar_empleado,
            fg_color="#3498db"
        )
        btn_registrar.grid(row=len(campos), columnspan=2, pady=15)

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
            headers = ["ID", "Nombre", "RFC", "Salario", "Departamento"]
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
                ctk.CTkLabel(self.scroll_frame, text=emp["departamento"]).grid(row=row, column=4, padx=10)
                
        except Exception as e:
            print(f"Error en _actualizar_lista: {e}")
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"Error al cargar datos: {str(e)}",
                text_color="red"
            ).pack()

    def _registrar_empleado(self):
        try:
            # 1. Obtener datos
            datos = {
                "nombre": self.entry_nombre.get(),
                "rfc": self.entry_rfc.get(),
                "salario": float(self.entry_salario.get()),
                "depto_id": int(self.entry_depto.get())
            }
            
            # 2. Validar campos vacíos
            if not all(datos.values()):
                print("⚠️ Todos los campos son obligatorios")
                return
                
            # 3. Registrar en backend
            if agregar_empleado(**datos):
                self._limpiar_formulario()
                self.tabs.set("📋 Lista de Empleados")
                self.after(500, self._actualizar_lista)
                self.mostrar_notificacion("✅ Empleado registrado con éxito")
            else:
                print("Error al Reistrar el Usuairo")
            
            
            # 5. Feedback visual (opcional)
            
            
        except Exception as e:
            print(f"❌ Error en datos: {str(e)}")
            self.mostrar_notificacion(f"Error: {str(e)}", error=True)

    def mostrar_notificacion(self, mensaje, error=False):
        """Muestra un mensaje flotante"""
        notif = ctk.CTkToplevel(self)
        notif.geometry("300x100")
        notif.title("Notificación")
        
        label = ctk.CTkLabel(
            notif, 
            text=mensaje,
            text_color="#e74c3c" if error else "#27ae60"
        )
        label.pack(pady=20)
        
        # Cierra automáticamente después de 2 segundos
        self.after(2000, notif.destroy)

    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_rfc.delete(0, "end")
        self.entry_salario.delete(0, "end")
        self.entry_depto.delete(0, "end")