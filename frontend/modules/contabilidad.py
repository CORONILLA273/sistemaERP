import customtkinter as ctk
from backend.logic.contabilidad import obtener_ingresos, obtener_egresos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
from datetime import datetime
import mplcursors



class ModuloContabilidad(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack_propagate(False)
        
        self.pack(expand=True, fill="both")
        self._crear_vista()

    def _crear_vista(self):
        
        titulo = ctk.CTkLabel(self, text="📊 Comparativa de Ingresos y Egresos", font=("Arial", 16, "bold"))
        titulo.pack(pady=(10, 5))

        ingresos = obtener_ingresos()
        egresos = obtener_egresos()

        fechas_crudas = sorted(set([i["fecha"] for i in ingresos] + [e["fecha"] for e in egresos]))
        fechas_crudas = [datetime.strptime(f, "%Y-%m-%d") for f in fechas_crudas]
        fechas = fechas_crudas[-5:]  # Solo los últimos 5 días con datos


        datos_ingresos = {datetime.strptime(i["fecha"], "%Y-%m-%d"): i["total"] for i in ingresos}
        datos_egresos = {datetime.strptime(e["fecha"], "%Y-%m-%d"): e["total"] for e in egresos}


        ingresos = [datos_ingresos.get(f, 0) for f in fechas]
        egresos = [datos_egresos.get(f, 0) for f in fechas]
        utilidad = [ingresos[i] - egresos[i] for i in range(len(fechas))]


        self.fig, ax = plt.subplots(figsize=(10, 5), facecolor="#f0f0f0")
        
        colores = {
            'ingresos': '#2ecc71',
            'egresos': '#e74c3c',    # Rojo intenso
            'utilidad': '#3498db'
        }
        ax.plot(fechas, ingresos, marker='o', markersize=8, linewidth=3, label="Ingresos", color=colores["ingresos"], alpha=0.9, markeredgecolor='white', markeredgewidth=1.5 )
        ax.plot(fechas, egresos, marker='s', linewidth=2, label="Egresos", color=colores["egresos"], alpha=0.9, markeredgecolor='white', markeredgewidth=1.5)
        ax.plot(fechas, utilidad, marker='^', markersize=8, linewidth=3, label="Utilidad Neta", color=colores["utilidad"], alpha=0.9, markeredgecolor='white', markeredgewidth=1.5)
        mplcursors.cursor(ax.lines, hover=True)
        def formato_moneda (x, pos):
            return f"{x:,.0f}"
        
        ax.yaxis.set_major_formatter(FuncFormatter(formato_moneda))

        ax.set_title("Balance Financiero por Fecha", fontsize=14, pad=20, fontweight='bold', color="#2c3e50")
        ax.set_ylabel("Monto (MXN)", fontsize=12, labelpad=10, color='#34495e')
        ax.set_xlabel("Fecha", fontsize=12, labelpad=10, color='#34495e')
        ax.set_title("Evolución Financiera")
        ax.legend()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tabla de resumen
        tabla_frame = ctk.CTkScrollableFrame(self, height=250)
        tabla_frame.pack(fill="both", expand=False, padx=10, pady=(5, 10))
        self.canvas = canvas
        # Encabezados
        encabezados = ["Fecha", "Ingresos", "Egresos", "Utilidad Neta"]
        for col, texto in enumerate(encabezados):
            ctk.CTkLabel(tabla_frame, text=texto, font=("Arial", 12, "bold"), text_color="#3498db").grid(row=0, column=col, padx=10, pady=5, sticky="ew")

        # Filas de datos
        for fila, f in enumerate(fechas, start=1):
            ctk.CTkLabel(tabla_frame, text=f.strftime("%Y-%m-%d")).grid(row=fila, column=0, padx=10, pady=2)
            ctk.CTkLabel(tabla_frame, text=f"${ingresos[fila-1]:.2f}").grid(row=fila, column=1, padx=10, pady=2)
            ctk.CTkLabel(tabla_frame, text=f"${egresos[fila-1]:.2f}").grid(row=fila, column=2, padx=10, pady=2)
            ctk.CTkLabel(tabla_frame, text=f"${utilidad[fila-1]:.2f}").grid(row=fila, column=3, padx=10, pady=2)
        
        self.canvas = None
    
    def destroy (self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if hasattr(self, "fig"):
            plt.close(self.fig)
        super().destroy()

