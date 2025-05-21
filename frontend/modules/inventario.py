import customtkinter as ctk
from backend.logic.inventario import agregar_producto, obtener_productos

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

        headers = ["ID", "Nombre", "Precio", "Stock"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(self.scroll, text=header, font=("Arial", 12, "bold"), text_color="#3498db" ).grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        for row, p in enumerate(productos, start=1):
            ctk.CTkLabel(self.scroll, text=str(p["id"])).grid(row=row, column=0, padx=10)
            ctk.CTkLabel(self.scroll, text=p["nombre"]).grid(row=row, column=1, padx=10)
            ctk.CTkLabel(self.scroll, text=f"${p['precio']:.2f}").grid(row=row, column=2, padx=10)
            ctk.CTkLabel(self.scroll, text=p["stock"]).grid(row=row, column=3, padx=10)

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
