
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
        self.parent = parent
        self.pack_propagate(False)

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

        # Encabezado
        encabezados = ["ID", "Fecha", "Proveedor", "Materia", "Cantidad", "Precio", "Total", "Acciones"]
        for col, texto in enumerate(encabezados):
            ctk.CTkLabel(self.scroll, text=texto, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        fila = 1
        for compra in compras:
            mostrar_datos_compra = True
            for materia in compra["materias"]:
                if mostrar_datos_compra:
                    ctk.CTkLabel(self.scroll, text=compra["id"]).grid(row=fila, column=0, padx=10)
                    ctk.CTkLabel(self.scroll, text=compra["fecha"]).grid(row=fila, column=1, padx=10)
                    ctk.CTkLabel(self.scroll, text=compra["proveedor"]).grid(row=fila, column=2, padx=10)
                    mostrar_datos_compra = False
                else:
                    # Dejar celdas vacías para ID, Fecha y Proveedor
                    ctk.CTkLabel(self.scroll, text="").grid(row=fila, column=0, padx=10)
                    ctk.CTkLabel(self.scroll, text="").grid(row=fila, column=1, padx=10)
                    ctk.CTkLabel(self.scroll, text="").grid(row=fila, column=2, padx=10)

                # Siempre mostrar los datos de la materia
                ctk.CTkLabel(self.scroll, text=materia["nombre"]).grid(row=fila, column=3, padx=10)
                ctk.CTkLabel(self.scroll, text=materia["cantidad"]).grid(row=fila, column=4, padx=10)
                ctk.CTkLabel(self.scroll, text=f"${materia['precio']:.2f}").grid(row=fila, column=5, padx=10)
                total_linea = materia["precio"] * materia["cantidad"]
                ctk.CTkLabel(self.scroll, text=f"${total_linea:.2f}").grid(row=fila, column=6, padx=10)

                if compra["materias"].index(materia) == 0:
                    boton = ctk.CTkButton(self.scroll, text="📄 Generar", width=90, command=lambda c=compra: self.generar_archivo_compra(c))
                    boton.grid(row=fila, column=7, padx=5)
                else:
                    ctk.CTkLabel(self.scroll, text="").grid(row=fila, column=7, padx=5)

                fila += 1

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

        cantidad = ctk.CTkEntry(fila, width=60)
        cantidad.pack(side="left", padx=5)
        cantidad.insert(0, "1")

        precio_label = ctk.CTkLabel(fila, text="$0.00", width=80)
        precio_label.pack(side="left", padx=5)

        subtotal_label = ctk.CTkLabel(fila, text="$0.00", width=80)
        subtotal_label.pack(side="left", padx=5)

        def actualizar():
            seleccion = combo.get()
            try:
                cant = int(cantidad.get())
            except ValueError:
                cant = 0

            if seleccion in materia_prices:
                precio = materia_prices[seleccion]
                precio_label.configure(text=f"${precio:.2f}")
                subtotal_label.configure(text=f"${precio * cant:.2f}")
            else:
                precio_label.configure(text="$0.00")
                subtotal_label.configure(text="$0.00")

        combo.bind("<<ComboboxSelected>>", lambda e: actualizar())
        cantidad.bind("<KeyRelease>", lambda e: actualizar())

        # Valor inicial si hay materias
        if materia_names:
            combo.set(materia_names[0])
            actualizar()

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

    def generar_archivo_compra(self, compra):
        try:
            contenido = f"Compra #{compra['id']}\nFecha: {compra['fecha']}\nProveedor: {compra['proveedor']}\n\nInsumos:\n"
            total = 0
            for insumo in compra["materias"]:
                subtotal = insumo["precio"] * insumo["cantidad"]
                contenido += f"- {insumo['nombre']} x {insumo['cantidad']} @ ${insumo['precio']:.2f} = ${subtotal:.2f}\n"
                total += subtotal
            contenido += f"\nTOTAL: ${total:.2f}"

            ruta = f"compra_{compra['id']}.txt"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)

            self._notificar(f"✅ Archivo generado: {ruta}")
        except Exception as e:
            self._notificar(f"❌ Error al generar archivo: {e}", error=True)

    
