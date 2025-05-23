import customtkinter as ctk
from backend.logic.rh import actualizar_empleado

class ModuloPerfil(ctk.CTkFrame):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self, text="👤 Mi Perfil", font=("Arial", 16, "bold")).pack(pady=(0, 10))

        datos = [
            ("Nombre", usuario.nombre),
            ("RFC", usuario.rfc),
            ("Salario", f"${usuario.salario:,.2f}"),
            ("Correo", usuario.correo),
            ("Departamento", usuario.departamento.nombre)
        ]

        for etiqueta, valor in datos:
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=f"{etiqueta}:", width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(frame, text=valor, anchor="w").pack(side="left")

        ctk.CTkLabel(self, text="Nueva Contraseña:", font=("Arial", 12)).pack(pady=(15, 5))
        self.entry_contra = ctk.CTkEntry(self, show="*", placeholder_text="********")
        self.entry_contra.pack(pady=5, fill="x")

        ctk.CTkButton(self, text="Actualizar Contraseña", command=self.actualizar_contra).pack(pady=10)

    def actualizar_contra(self):
        nueva = self.entry_contra.get().strip()
        if not nueva or len(nueva) < 4:
            self._mensaje("La contraseña debe tener al menos 4 caracteres.", error=True)
            return

        if actualizar_empleado(self.usuario.id, self.usuario.nombre, self.usuario.rfc, self.usuario.salario, self.usuario.departamento.id, nueva):
            self._mensaje("✅ Contraseña actualizada correctamente.")
        else:
            self._mensaje("❌ Error al actualizar la contraseña.", error=True)

    def _mensaje(self, msg, error=False):
        top = ctk.CTkToplevel(self)
        top.title("Aviso")
        ctk.CTkLabel(top, text=msg, text_color="red" if error else "green").pack(pady=10)
        ctk.CTkButton(top, text="Aceptar", command=top.destroy).pack(pady=5)
