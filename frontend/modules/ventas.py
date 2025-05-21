import customtkinter as ctk
from backend.logic.ventas import (
    obtener_ventas, registrar_venta,
    obtener_o_crear_cliente_por_nombre, obtener_vendedores,
    obtener_productos_disponibles
)

class ModuloVentas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")
        
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_lista = self.tabs.add("📋 Lista de Ventas")
        self.tab_registro = self.tabs.add("➕ Registrar Venta")
        
        self._crear_lista_ventas()
        self._crear_formulario_registro()

    def _crear_lista_ventas(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_lista)
        self.scroll_frame.pack(expand=True, fill="both")
        self._actualizar_lista()

    def _actualizar_lista(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        ventas = obtener_ventas()
        if not ventas:
            ctk.CTkLabel(self.scroll_frame, text="No hay ventas registradas.").pack(pady=20)
            return

        encabezados = ["ID", "Fecha", "Cliente", "Vendedor", "Producto", "Cantidad", "Precio", "Subtotal", "Acciones"]
        for col, texto in enumerate(encabezados):
            ctk.CTkLabel(self.scroll_frame, text=texto, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        fila = 1
        for venta in ventas:
            mostrar_venta = True
            for producto in venta["productos"]:
                if mostrar_venta:
                    ctk.CTkLabel(self.scroll_frame, text=venta["id"]).grid(row=fila, column=0, padx=10)
                    ctk.CTkLabel(self.scroll_frame, text=venta["fecha"]).grid(row=fila, column=1, padx=10)
                    ctk.CTkLabel(self.scroll_frame, text=venta["cliente"]).grid(row=fila, column=2, padx=10)
                    ctk.CTkLabel(self.scroll_frame, text=venta["vendedor"]).grid(row=fila, column=3, padx=10)
                    boton = ctk.CTkButton(self.scroll_frame, text="📄 Generar", width=90, command=lambda v=venta: self.generar_archivo_venta(v))
                    boton.grid(row=fila, column=8, padx=5)
                    mostrar_venta = False
                else:
                    for col in range(4):
                        ctk.CTkLabel(self.scroll_frame, text="").grid(row=fila, column=col, padx=10)

                ctk.CTkLabel(self.scroll_frame, text=producto["nombre"]).grid(row=fila, column=4, padx=10)
                ctk.CTkLabel(self.scroll_frame, text=producto["cantidad"]).grid(row=fila, column=5, padx=10)
                ctk.CTkLabel(self.scroll_frame, text=f"${producto['precio_unitario']:.2f}").grid(row=fila, column=6, padx=10)
                subtotal = producto["precio_unitario"] * producto["cantidad"]
                ctk.CTkLabel(self.scroll_frame, text=f"${subtotal:.2f}").grid(row=fila, column=7, padx=10)
                    
                fila += 1

               

    
    def _crear_formulario_registro(self):
        self.form_frame = ctk.CTkFrame(self.tab_registro)
        self.form_frame.pack(padx=20, pady=20, fill="x")

        ctk.CTkLabel(self.form_frame, text="Nombre del Cliente").pack(anchor="w", pady=(10, 0), padx=5)
        self.entry_cliente = ctk.CTkEntry(self.form_frame, placeholder_text="Ej. Juan Pérez")
        self.entry_cliente.pack(pady=5, padx=5, fill="x")

        self.vendedores = {nombre: id for id, nombre in obtener_vendedores()}    
        ctk.CTkLabel(self.form_frame, text="Vendedor (Empleado del área de Ventas)").pack(anchor="w", pady=(10, 0), padx=5)
        self.combo_vendedor = ctk.CTkComboBox(self.form_frame, values=list(self.vendedores.keys()), state="readonly")
        self.combo_vendedor.pack(pady=5, padx=5, fill="x")
        self.combo_vendedor.set("")

        ctk.CTkLabel(self.form_frame, text="Productos").pack(anchor="w", pady=(10, 0), padx=5)
        self.productos_disponibles = obtener_productos_disponibles()
        self.product_inputs = []

        self.frame_productos = ctk.CTkScrollableFrame(self.form_frame, height=200)
        self.frame_productos.pack(pady=5, padx=5, fill="x")
        self._agregar_producto_input()  # Inicial

        ctk.CTkButton(self.form_frame, text="➕ Agregar Producto", command=self._agregar_producto_input).pack(pady=5)
        ctk.CTkButton(self.form_frame, text="💾 Registrar Venta", fg_color="#2ecc71", command=self._registrar_venta).pack(pady=10)

    def _agregar_producto_input(self):
        producto_names = [f"{p['nombre']} (${p['precio']:.2f} / Stock: {p['stock']})" for p in self.productos_disponibles]
        producto_ids = {f"{p['nombre']} (${p['precio']:.2f} / Stock: {p['stock']})": p['id'] for p in self.productos_disponibles}

        fila = ctk.CTkFrame(self.frame_productos)
        fila.pack(pady=4, padx=5, fill="x")

        combo = ctk.CTkComboBox(fila, values=producto_names, width=300, state="readonly")
        combo.pack(side="left", padx=5)
        combo.set("")

        cantidad = ctk.CTkEntry(fila, width=60)
        cantidad.pack(side="left", padx=5)
        cantidad.insert(0, "1")

        self.product_inputs.append((combo, cantidad, producto_ids))

    def _registrar_venta(self):
        try:
            cliente_nombre = self.entry_cliente.get().strip()
            vendedor = self.combo_vendedor.get()

            if not cliente_nombre:
                raise ValueError("Debe Ingresar el nombre del cliente")

            cliente_id = obtener_o_crear_cliente_por_nombre(cliente_nombre)
            if not cliente_id:
                raise RuntimeError("No se pudo registrar o encontrar el cliente")
            if not cliente_nombre or not vendedor:
                raise ValueError("Selecciona cliente y vendedor")

            vendedor_id = self.vendedores[vendedor]

            productos = []
            for combo, entry, ids in self.product_inputs:
                key = combo.get()
                if key not in ids:
                    continue
                producto_id = ids[key]
                try:
                    cantidad = int(entry.get())
                    if cantidad <= 0:
                        raise ValueError()
                except:
                    raise ValueError("Cantidad inválida")

                productos.append({"producto_id": producto_id, "cantidad": cantidad})

            if not productos:
                raise ValueError("Debe agregar al menos un producto")

            if registrar_venta(cliente_id, vendedor_id, productos):
                self.mostrar_notificacion("✅ Venta registrada")
                self._resetear_formulario()
                self._actualizar_lista()
                self.tabs.set("📋 Lista de Ventas")
            else:
                raise RuntimeError("No se pudo registrar la venta")

        except Exception as e:
            self.mostrar_notificacion(f"❌ {str(e)}", error=True)

    def mostrar_notificacion(self, mensaje, error=False):
        notif = ctk.CTkToplevel(self)
        notif.title("Error" if error else "Éxito")
        notif.geometry("400x100")
        notif.resizable(False, False)

        ctk.CTkLabel(notif, text=mensaje, text_color="#e74c3c" if error else "#2ecc71").pack(pady=10)
        ctk.CTkButton(notif, text="OK", command=notif.destroy).pack()

    def _resetear_formulario(self):
        self.entry_cliente.delete(0, "end")
        self.combo_vendedor.set("")
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        self.product_inputs.clear()
        self._agregar_producto_input()

    def generar_archivo_venta(self, venta):
        try:
            contenido = f"Venta #{venta['id']}\nFecha: {venta['fecha']}\nCliente: {venta['cliente']}\nVendedor: {venta['vendedor']}\n\nProductos:\n"
            total = 0
            for prod in venta["productos"]:
                subtotal = prod["precio_unitario"] * prod["cantidad"]
                contenido += f"- {prod['nombre']} x {prod['cantidad']} @ ${prod['precio_unitario']:.2f} = ${subtotal:.2f}\n"
                total += subtotal
            contenido += f"\nTOTAL: ${total:.2f}"

            ruta = f"venta_{venta['id']}.txt"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)

            self.mostrar_notificacion(f"✅ Archivo generado: {ruta}")
        except Exception as e:
            self.mostrar_notificacion(f"❌ Error al generar archivo: {e}", error=True)



