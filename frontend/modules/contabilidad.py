import customtkinter as ctk
from backend.logic.contabilidad import obtener_ingresos, obtener_egresos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ModuloContabilidad(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")
        self._crear_vista()

    def _crear_vista(self):
        titulo = ctk.CTkLabel(self, text="📊 Comparativa de Ingresos y Egresos", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        ingresos = obtener_ingresos()
        egresos = obtener_egresos()

        fechas = sorted(set([i["fecha"] for i in ingresos] + [e["fecha"] for e in egresos]))

        datos_ingresos = {i["fecha"]: i["total"] for i in ingresos}
        datos_egresos = {e["fecha"]: e["total"] for e in egresos}

        ingresos = [datos_ingresos.get(f, 0) for f in fechas]
        egresos = [datos_egresos.get(f, 0) for f in fechas]
        utilidad = [ingresos[i] - egresos[i] for i in range(len(fechas))]


        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(fechas, ingresos, marker='o', label="Ingresos", linewidth=2)
        ax.plot(fechas, egresos, marker='s', label="Egresos", linewidth=2)
        ax.plot(fechas, utilidad, marker='^', label="Utilidad Neta", linewidth=2)

        ax.set_title("Balance Financiero por Fecha")
        ax.set_ylabel("Monto (MXN)")
        ax.set_xlabel("Fecha")
        ax.set_title("Ingresos vs Egresos por Fecha")
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tabla de resumen
        tabla_frame = ctk.CTkFrame(self)
        tabla_frame.pack(fill="both", expand=False, padx=10, pady=(5, 10))

        # Encabezados
        encabezados = ["Fecha", "Ingresos", "Egresos", "Utilidad Neta"]
        for col, texto in enumerate(encabezados):
            ctk.CTkLabel(tabla_frame, text=texto, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        # Filas de datos
        for fila, f in enumerate(fechas, start=1):
            ctk.CTkLabel(tabla_frame, text=f).grid(row=fila, column=0, padx=10, pady=2)
            ctk.CTkLabel(tabla_frame, text=f"${ingresos[fila-1]:.2f}").grid(row=fila, column=1, padx=10, pady=2)
            ctk.CTkLabel(tabla_frame, text=f"${egresos[fila-1]:.2f}").grid(row=fila, column=2, padx=10, pady=2)
            ctk.CTkLabel(tabla_frame, text=f"${utilidad[fila-1]:.2f}").grid(row=fila, column=3, padx=10, pady=2)

