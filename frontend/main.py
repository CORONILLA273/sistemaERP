import customtkinter as ctk
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from modules.rh import ModuloRH
from modules.ventas import ModuloVentas
from modules.inventario import ModuloInventario

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

    def crearBotonesMenu(self):
        # Confiuración para botones
        botonConfig = {
            "master": self.menuLateral,
            "height":40,
            "corner_radius": 8,
            "anchor": "w"
        }

        # Botones
        ctk.CTkLabel(self.menuLateral, text="Módulos", font=("Arial", 18)).pack(pady=20, padx=10)

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

        ctk.CTkLabel(self.contenedorPrincipal, text="Módulo de Compras").pack()
    
    def mostrarModuloInventario(self):
        self.limpiar()

        ModuloInventario(self.contenedorPrincipal).pack(expand=True, fill="both")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()