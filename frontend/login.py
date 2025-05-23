import customtkinter as ctk
import sys
from pathlib import Path
from PIL import Image

# Agrega el directorio raíz del proyecto al path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.database import Session, Empleado

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - ERP BNJ")
        self.geometry("400x450")
        self.state("zoomed")
        self.resizable(True, True)
        

        ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 20, "bold")).pack(pady=20)
        ruta_imagen = "frontend/widgets/logo-bnj.png"
        img = ctk.CTkImage(light_image=Image.open(ruta_imagen), size=(300, 100))

        # Mostrar la imagen
        ctk.CTkLabel(self, image=img, text="").pack(pady=10)
        self.image_banner = img

        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Correo")
        self.entry_correo.pack(pady=10, padx=20, fill="x")

        self.entry_contraseña = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_contraseña.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self, text="Ingresar", command=self.autenticar).pack(pady=20)
        recuperar = ctk.CTkLabel(self, text="¿Olvidaste tu contraseña?", text_color="#3498db", cursor="hand2")
        recuperar.pack(pady=(5, 20))
        recuperar.bind("<Button-1>", lambda e: self.recuperar_contraseña())
    
    def recuperar_contraseña(self):
        top = ctk.CTkToplevel(self)
        top.title("Recuperar Contraseña")
        top.geometry("350x220")
        top.grab_set()

        ctk.CTkLabel(top, text="Ingresa tu correo:", font=("Arial", 12)).pack(pady=10)
        entry_email = ctk.CTkEntry(top, placeholder_text="correo@ejemplo.com")
        entry_email.pack(pady=5, padx=10, fill="x")

        resultado_label = ctk.CTkLabel(top, text="", text_color="white", wraplength=300)
        resultado_label.pack(pady=5)

        def buscar():
            correo = entry_email.get().strip()
            if not correo:
                resultado_label.configure(text="Campo vacío", text_color="red")
                return

            session = Session()
            try:
                empleado = session.query(Empleado).filter_by(correo=correo).first()
                if empleado:
                    resultado_label.configure(text=f"Tu contraseña es: {empleado.contraseña}", text_color="#27ae60")
                else:
                    resultado_label.configure(text="Correo no encontrado", text_color="red")
            finally:
                session.close()

        ctk.CTkButton(top, text="Recuperar", command=buscar).pack(pady=10)
        ctk.CTkButton(top, text="Cerrar", command=top.destroy).pack(pady=5)

    def autenticar(self):
        correo = self.entry_correo.get().strip()
        clave = self.entry_contraseña.get().strip()

        if not correo or not clave:
            self._alerta("Por favor, complete ambos campos.")
            return

        session = Session()
        try:
            empleado = session.query(Empleado).filter_by(correo=correo, contraseña=clave).first()
            if empleado:
                self.destroy()
                from frontend.main import App
                app = App(usuario=empleado)  # Paso del empleado autenticado
                app.mainloop()
            else:
                self._alerta("Credenciales inválidas.")
        finally:
            session.close()

    def _alerta(self, msg):
        top = ctk.CTkToplevel(self)
        ctk.CTkLabel(top, text=msg, text_color="red").pack(pady=10)
        ctk.CTkButton(top, text="Cerrar", command=top.destroy).pack(pady=5)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = LoginScreen()
    app.mainloop()