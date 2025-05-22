import customtkinter as ctk
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from modules.rh import ModuloRH
from modules.ventas import ModuloVentas
from modules.inventario import ModuloInventario
from modules.compras import ModuloCompras
from modules.contabilidad import ModuloContabilidad
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERP Bombas BNJ")
        self.geometry("1200x700")
        ctk.set_appearance_mode("dark")

        # Creación de sidebar
        self.menuLateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menuLateral.pack(side="left", fill="y")
        self.menuLateral.pack_propagate(False)

        # Área de los módulos
        self.contenedorPrincipal = ctk.CTkFrame(self)
        self.contenedorPrincipal.pack(side="right", expand=True, fill="both")

        self.crearBotonesMenu()

        self.mostrarModuloRh()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)


    def crearBotonesMenu(self):
        # Confiuración para botones
        botonConfig = {
            "master": self.menuLateral,
            "height":40,
            "corner_radius": 8,
            "anchor": "w"
        }

        # Botones
        imagen_path = "frontend/widgets/logo2.png"  # Ajusta la ruta según tu imagen
        img = ctk.CTkImage(light_image=Image.open(imagen_path), size=(180, 110))  # ajusta tamaño

        ctk.CTkLabel(self.menuLateral, image=img, text="").pack(pady=20)

        ctk.CTkButton(
            **botonConfig,
            text="Recusros Humanos",
            command= self.mostrarModuloRh
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            **botonConfig,
            text="Ventas",
            command= self.mostrarModuloVentas
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            **botonConfig,
            text="Compras",
            command= self.mostrarModuloCompras
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            **botonConfig,
            text="Inventario",
            command= self.mostrarModuloInventario
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            **botonConfig,
            text="Finanzas",
            command= self.mostrarModuloContabilidad
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            **botonConfig,
            text="Salir",
            command= self.destroy,
            fg_color="#d9534f",
            hover_color="#c9302c"
        ).pack(pady=5, padx=10)

    def limpiar(self):
        """Destruye todos los widgets dentro del contenedor principal"""
        for widget in self.contenedorPrincipal.winfo_children():
            widget.destroy()

    def mostrarModuloRh(self):
        self.limpiar()
        ModuloRH(self.contenedorPrincipal).pack(expand=True, fill= "both")

    def mostrarModuloVentas(self):
        self.limpiar()

        ModuloVentas(self.contenedorPrincipal).pack(expand=True, fill="both")

    def mostrarModuloCompras(self):
        self.limpiar()

        ModuloCompras(self.contenedorPrincipal).pack(expand=True, fill="both")
    
    def mostrarModuloInventario(self):
        self.limpiar()

        ModuloInventario(self.contenedorPrincipal).pack(expand=True, fill="both")
    
    def mostrarModuloContabilidad(self):
        self.limpiar()

        ModuloContabilidad(self.contenedorPrincipal).pack(expand=True, fill="both")
    def cerrar_aplicacion(self):
        for widget in self.contenedorPrincipal.winfo_children():
            if hasattr(widget, 'destroy'):
                widget.destroy()
        try:
            import matplotlib.pyplot as plt
            plt.close("all")  # Cierra cualquier figura activa de matplotlib
        except:
            pass
        self.destroy()
    

if __name__ == "__main__":
    try:
        ctk.set_appearance_mode("dark")
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
