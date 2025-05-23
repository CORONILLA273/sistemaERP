import customtkinter as ctk
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from modules.rh import ModuloRH
from modules.ventas import ModuloVentas
from modules.inventario import ModuloInventario
from modules.compras import ModuloCompras
from modules.contabilidad import ModuloContabilidad
from modules.perfil import ModuloPerfil
from PIL import Image

class App(ctk.CTk):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario
        self.title("ERP Bombas BNJ")
        self.geometry("1200x600")
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
        
        nombre_usuario = f"👤 {self.usuario.nombre}\n📁 {self.usuario.departamento.nombre}" if self.usuario else "Usuario"
        ctk.CTkLabel(self.menuLateral, text=nombre_usuario, font=("Arial", 14)).pack(pady=(10, 5))

        permisos = {
            "Recursos Humanos": [self.mostrarModuloRh],
            "Ventas": [self.mostrarModuloVentas, self.mostrarModuloInventario],
            "Compras": [self.mostrarModuloCompras],
            "Producción": [self.mostrarModuloInventario],
            "Contabilidad": [self.mostrarModuloContabilidad, self.mostrarModuloCompras, self.mostrarModuloVentas],
            "Dirección": [self.mostrarModuloRh, self.mostrarModuloVentas, self.mostrarModuloCompras,
                        self.mostrarModuloInventario, self.mostrarModuloContabilidad],
        }

        # Obtener nombre del departamento del usuario
        depto = self.usuario.departamento.nombre if self.usuario and self.usuario.departamento else ""
        # Mapear texto a función y nombre para el botón
        opciones = {
            self.mostrarModuloRh: "Recursos Humanos",
            self.mostrarModuloVentas: "Ventas",
            self.mostrarModuloCompras: "Compras",
            self.mostrarModuloInventario: "Inventario",
            self.mostrarModuloContabilidad: "Finanzas"
        }

        for funcion in permisos.get(depto, []):
            ctk.CTkButton(**botonConfig, text=opciones[funcion], command=funcion).pack(pady=5, padx=10)

        if depto not in ["Recursos Humanos", "Dirección"]:
            ctk.CTkButton(**botonConfig, text="Mi Perfil", command=self.mostrarModuloPerfil).pack(pady=5, padx=10)

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

        ModuloVentas(self.contenedorPrincipal, self.usuario).pack(expand=True, fill="both")

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
    
    def mostrarModuloPerfil(self):
        self.limpiar()
        ModuloPerfil(self.contenedorPrincipal, self.usuario).pack(expand=True, fill="both")

    

if __name__ == "__main__":
    try:
        ctk.set_appearance_mode("dark")
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
