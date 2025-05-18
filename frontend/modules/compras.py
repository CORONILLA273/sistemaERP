# frontend/ModuloCompras.py

import customtkinter as ctk
from backend.logic.compras import (
    obtener_compras,
    obtener_materias_primas,
    obtener_proveedores,
    registrar_compra,
    registrar_proveedor
)

class ModuloCompras(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_lista = self.tabs.add("📋 Lista de Compras")
        self.tab_registro = self.tabs.add("➕ Registrar Compra")
        self.tab_proveedor = self.tabs.add("🛒 Registrar Proveedor")

        self._crear_lista()
        self._crear_formulario()
        self._crear_formulario_proveedor()

    def _crear_lista(self):
        self.scroll = ctk.CTkScrollableFrame(self.tab_lista)
        self.scroll.pack(expand=True, fill="both")
        self._actualizar_lista()

    def _actualizar_lista(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        compras = obtener_compras()
        if not compras:
            ctk.CTkLabel(self.scroll, text="No hay compras registradas.").pack(pady=20)
            return

        for compra in compras:
            frame = ctk.CTkFrame(self.scroll)
            frame.pack(padx=10, pady=10, fill="x")

            encabezado = f"Compra #{compra['id']} - {compra['fecha']} - Proveedor: {compra['proveedor']} - Total: ${compra['total']:.2f}"
            ctk.CTkLabel(frame, text=encabezado, font=("Arial", 12, "bold")).pack(anchor="w")

            for prod in compra['materias']:
                detalle = f"- {prod['nombre']} x {prod['cantidad']} @ ${prod['precio']:.2f}"
                ctk.CTkLabel(frame, text=detalle, font=("Arial", 11)).pack(anchor="w")

    def _crear_formulario(self):
        self.form_frame = ctk.CTkFrame(self.tab_registro)
        self.form_frame.pack(padx=20, pady=20, fill="x")

        self.proveedores = {nombre: id for id, nombre in obtener_proveedores()}

        ctk.CTkLabel(self.form_frame, text="Proveedor").pack(anchor="w", pady=(10, 0), padx=5)
        self.combo_proveedor = ctk.CTkComboBox(self.form_frame, values=list(self.proveedores.keys()), state="readonly")
        self.combo_proveedor.pack(pady=5, fill="x")
        self.combo_proveedor.set("")

        ctk.CTkLabel(self.form_frame, text="Insumos").pack(anchor="w", pady=(10, 0), padx=5)
        self.materias_disponibles = obtener_materias_primas()
        self.materia_inputs = []

        self.frame_materias = ctk.CTkScrollableFrame(self.form_frame, height=200)
        self.frame_materias.pack(pady=5, fill="x")
        self._agregar_materia_input()

        ctk.CTkButton(self.form_frame, text="➕ Agregar materia", command=self._agregar_materia_input).pack(pady=5)
        ctk.CTkButton(self.form_frame, text="💾 Registrar Compra", fg_color="#27ae60", command=self._registrar_compra).pack(pady=10)

    def _crear_formulario_proveedor(self):
        self.form_proveedor = ctk.CTkFrame(self.tab_proveedor)
        self.form_proveedor.pack(padx=20, pady=20, fill="x")

        # Campos del formulario
        self.entry_nombre_prov = ctk.CTkEntry(self.form_proveedor, placeholder_text="Nombre del proveedor")
        self.entry_contacto_prov = ctk.CTkEntry(self.form_proveedor, placeholder_text="Contacto")
        self.entry_telefono_prov = ctk.CTkEntry(self.form_proveedor, placeholder_text="Teléfono")

        self.entry_nombre_prov.pack(pady=5, fill="x")
        self.entry_contacto_prov.pack(pady=5, fill="x")
        self.entry_telefono_prov.pack(pady=5, fill="x")

        ctk.CTkButton(
            self.form_proveedor,
            text="Registrar Proveedor",
            fg_color="#27ae60",
            command=self._registrar_proveedor
        ).pack(pady=10)


    def _agregar_materia_input(self):
        materia_names = [f"{m['nombre']} ({m['unidad']})" for m in self.materias_disponibles]
        materia_ids = {f"{m['nombre']} ({m['unidad']})": m['id'] for m in self.materias_disponibles}
        materia_prices = {f"{m['nombre']} ({m['unidad']})": m['precio'] for m in self.materias_disponibles}

        fila = ctk.CTkFrame(self.frame_materias)
        fila.pack(pady=4, fill="x", padx=5)

        combo = ctk.CTkComboBox(fila, values=materia_names, width=300, state="readonly")
        combo.pack(side="left", padx=5)
        combo.set("")

        cantidad = ctk.CTkEntry(fila, width=60)
        cantidad.pack(side="left", padx=5)
        cantidad.insert(0, "1")

        precio_label = ctk.CTkLabel(fila, text="$0.00", width=80)
        precio_label.pack(side="left", padx=5)

        def actualizar_precio(event=None):
            seleccion = combo.get()
            if seleccion in materia_prices:
                precio_label.configure(text=f"${materia_prices[seleccion]:.2f}")

        combo.bind("<<ComboboxSelected>>", actualizar_precio)

        self.materia_inputs.append((combo, cantidad, precio_label, materia_ids, materia_prices))

    def _registrar_compra(self):
        try:
            proveedor_nombre = self.combo_proveedor.get().strip()
            if not proveedor_nombre:
                raise ValueError("Seleccione un proveedor")

            proveedor_id = self.proveedores[proveedor_nombre]

            materias = []
            for combo, entry_cantidad, precio_label, ids, prices in self.materia_inputs:
                key = combo.get()
                if key not in ids:
                    continue
                id = ids[key]
                precio = prices[key]  # ✅ Tomado directamente

                try:
                    cantidad = int(entry_cantidad.get())
                    if cantidad <= 0 or precio <= 0:
                        raise ValueError()
                except:
                    raise ValueError("Cantidad o precio inválido")

                materias.append({
                    "materia_id": id,
                    "cantidad": cantidad,
                    "precio": precio
                })

            if not materias:
                raise ValueError("Debe agregar al menos un materia")

            if registrar_compra(proveedor_id, materias):
                self._notificar("✅ Compra registrada")
                self._resetear_formulario()
                self._actualizar_lista()
                self.tabs.set("📋 Lista de Compras")
            else:
                raise RuntimeError("No se pudo registrar la compra")

        except Exception as e:
            self._notificar(f"❌ {str(e)}", error=True)

    def _registrar_proveedor(self):
        nombre = self.entry_nombre_prov.get().strip()
        contacto = self.entry_contacto_prov.get().strip()
        telefono = self.entry_telefono_prov.get().strip()

        if not nombre:
            self._notificar("❌ El nombre es obligatorio", error=True)
            return

        if registrar_proveedor(nombre, contacto, telefono):
            self._notificar("✅ Proveedor registrado correctamente")
            self.entry_nombre_prov.delete(0, "end")
            self.entry_contacto_prov.delete(0, "end")
            self.entry_telefono_prov.delete(0, "end")
            self.proveedores = {nombre: id for id, nombre in obtener_proveedores()}
            self.combo_proveedor.configure(values=list(self.proveedores.keys()))
        else:
            self._notificar("❌ No se pudo registrar el proveedor", error=True)


    def _resetear_formulario(self):
        self.combo_proveedor.set("")
        for widget in self.frame_materias.winfo_children():
            widget.destroy()
        self.materia_inputs.clear()
        self._agregar_materia_input()

    def _notificar(self, msg, error=False):
        top = ctk.CTkToplevel(self)
        top.title("Error" if error else "Éxito")
        ctk.CTkLabel(top, text=msg, text_color="#e74c3c" if error else "#27ae60").pack(pady=10)
        ctk.CTkButton(top, text="OK", command=top.destroy).pack(pady=5)
