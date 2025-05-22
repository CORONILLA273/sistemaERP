import customtkinter as ctk
from backend.logic.inventario import agregar_producto, obtener_productos, actualizar_producto, eliminar_producto

class ModuloInventario(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack_propagate(False)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_lista = self.tabs.add("📋 Lista de Productos")
        self.tab_registro = self.tabs.add("➕ Registrar Producto")

        self._crear_lista()
        self._crear_formulario()

    def _crear_lista(self):
        self.scroll = ctk.CTkScrollableFrame(self.tab_lista)
        self.scroll.pack(expand=True, fill="both")
        self._actualizar_lista()

    def _actualizar_lista(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        productos = obtener_productos()
        if not productos:
            ctk.CTkLabel(self.scroll, text="No hay productos registrados.").pack(pady=20)
            return

        headers = ["ID", "Nombre", "Precio", "Stock", "Acciones"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(self.scroll, text=header, font=("Arial", 12, "bold"), text_color="#3498db" ).grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        for row, p in enumerate(productos, start=1):
            ctk.CTkLabel(self.scroll, text=str(p["id"])).grid(row=row, column=0, padx=10)
            ctk.CTkLabel(self.scroll, text=p["nombre"]).grid(row=row, column=1, padx=10)
            ctk.CTkLabel(self.scroll, text=f"${p['precio']:.2f}").grid(row=row, column=2, padx=10)
            ctk.CTkLabel(self.scroll, text=p["stock"]).grid(row=row, column=3, padx=10)
            btn_editar = ctk.CTkButton(self.scroll, text="Actualizar", width=32, height=24, command=lambda prod=p: self._editar_producto(p))
            btn_editar.grid(row=row, column=4, padx=(5, 2), pady=5)

            btn_borrar = ctk.CTkButton(self.scroll, text="Eliminar", width=32, height=24, fg_color="#e74c3c",
                                        hover_color="#c0392b", command=lambda pr=p: self._confirmar_eliminar(pr["id"]))
            btn_borrar.grid(row=row, column=5, padx=(5, 2), pady=5)
    def _crear_formulario(self):
        frame = ctk.CTkFrame(self.tab_registro)
        frame.pack(pady=20, padx=20, fill="x")

        self.entry_nombre = ctk.CTkEntry(frame, placeholder_text="Nombre del Producto")
        self.entry_precio = ctk.CTkEntry(frame, placeholder_text="Precio (ej. 199.99)")
        self.entry_stock = ctk.CTkEntry(frame, placeholder_text="Stock inicial (ej. 50)")

        self.entry_nombre.pack(pady=5, fill="x")
        self.entry_precio.pack(pady=5, fill="x")
        self.entry_stock.pack(pady=5, fill="x")

        ctk.CTkButton(frame, text="Registrar Producto", command=self._registrar_producto, fg_color="#27ae60").pack(pady=10)

    def _registrar_producto(self):
        nombre = self.entry_nombre.get().strip()
        precio_text = self.entry_precio.get().strip()
        stock_text = self.entry_stock.get().strip()

        try:
            if not all([nombre, precio_text, stock_text]):
                raise ValueError("Todos los campos son obligatorios")

            precio = float(precio_text)
            stock = int(stock_text)
            if precio <= 0 or stock < 0:
                raise ValueError("Valores inválidos")
            productos_actuales = [p["nombre"].lower() for p in obtener_productos()]
            if nombre.lower() in productos_actuales:
                raise ValueError("Ya existe un producto con ese nombre")

            if agregar_producto(nombre, precio, stock):
                self._actualizar_lista()
                self._notificar("✅ Producto agregado correctamente")
                self.entry_nombre.delete(0, "end")
                self.entry_precio.delete(0, "end")
                self.entry_stock.delete(0, "end")
            else:
                raise RuntimeError("No se pudo registrar el producto")

        except Exception as e:
            self._notificar(f"❌ {str(e)}", error=True)

    def _notificar(self, mensaje, error=False):
        top = ctk.CTkToplevel(self)
        top.title("Error" if error else "Éxito")
        ctk.CTkLabel(top, text=mensaje, text_color="#e74c3c" if error else "#27ae60").pack(pady=10)
        ctk.CTkButton(top, text="Aceptar", command=top.destroy).pack(pady=5)
    def _editar_producto(self, producto):
        top = ctk.CTkToplevel(self)
        top.title("Editar Producto")
        top.geometry("300x250")

        ctk.CTkLabel(top, text="Editar Producto", font=("Arial", 14, "bold")).pack(pady=10)

        entry_nombre = ctk.CTkEntry(top)
        entry_nombre.insert(0, producto["nombre"])
        entry_nombre.pack(pady=5, fill="x", padx=10)

        entry_precio = ctk.CTkEntry(top)
        entry_precio.insert(0, str(producto["precio"]))
        entry_precio.pack(pady=5, fill="x", padx=10)

        entry_stock = ctk.CTkEntry(top)
        entry_stock.insert(0, str(producto["stock"]))
        entry_stock.pack(pady=5, fill="x", padx=10)

        def guardar():
            try:
                nuevo_nombre = entry_nombre.get().strip()
                nuevo_precio = float(entry_precio.get().strip())
                nuevo_stock = int(entry_stock.get().strip())

                if not nuevo_nombre or nuevo_precio <= 0 or nuevo_stock < 0:
                    raise ValueError()

                if actualizar_producto(producto["id"], nuevo_nombre, nuevo_precio, nuevo_stock):
                    top.destroy()
                    self._actualizar_lista()
                    self._notificar("✅ Producto actualizado correctamente")
                else:
                    self._notificar("❌ No se pudo actualizar", error=True)

            except:
                self._notificar("❌ Datos inválidos", error=True)

        ctk.CTkButton(top, text="Guardar", command=guardar, fg_color="#27ae60").pack(pady=10)

    def _confirmar_eliminar(self, producto_id):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Confirmar eliminación")
        ventana.geometry("300x120")

        ctk.CTkLabel(ventana, text="¿Deseas eliminar este producto?", font=("Arial", 12)).pack(pady=10)
        ctk.CTkButton(ventana, text="Eliminar", fg_color="#e74c3c", command=lambda: self._eliminar_producto(producto_id, ventana)).pack(pady=5)
        ctk.CTkButton(ventana, text="Cancelar", command=ventana.destroy).pack()

    def _eliminar_producto(self, producto_id, ventana):
        if eliminar_producto(producto_id):
                ventana.destroy()
                self._actualizar_lista()
                self._notificar("✅ Producto eliminado")
        else:
            self._notificar("❌ No se pudo eliminar", error=True)
    