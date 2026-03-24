import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import logic 
from PIL import Image
import reports # Importamos el nuevo módulo

# Configuración visual [cite: 5, 6]
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class AppFinanzas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Finanzas Personales")
        self.geometry("900x600")

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar [cite: 5]
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Mi Billetera", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)
        
        self.btn_grafico = ctk.CTkButton(self.sidebar, text="📊 Ver Gráficos", command=self.mostrar_ventana_grafico)
        self.btn_grafico.pack(pady=10, padx=20)

        # Reloj Sincronizado [cite: 7]
        self.reloj_label = ctk.CTkLabel(self.sidebar, text="", font=("Arial", 14))
        self.reloj_label.pack(pady=10)
        self.actualizar_reloj()

        # Botones
        self.btn_resumen = ctk.CTkButton(self.sidebar, text="Resumen", command=self.mostrar_resumen)
        self.btn_resumen.pack(pady=10, padx=20)

        self.btn_movimiento = ctk.CTkButton(self.sidebar, text="Nuevo Movimiento", command=self.crear_formulario_movimiento)
        self.btn_movimiento.pack(pady=10, padx=20)

        # Frame Principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.mostrar_resumen()

    def actualizar_reloj(self):
        self.reloj_label.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self.actualizar_reloj)

    def mostrar_resumen(self):
        for widget in self.main_frame.winfo_children(): widget.destroy()
        balance = logic.obtener_balance_total()
        color = "#2ecc71" if balance >= 0 else "#e74c3c"
        
        ctk.CTkLabel(self.main_frame, text="Balance Total", font=("Arial", 24)).pack(pady=20)
        ctk.CTkLabel(self.main_frame, text=f"${balance:,.0f} CLP", font=("Arial", 40, "bold"), text_color=color).pack(pady=10)

    def crear_formulario_movimiento(self):
        for widget in self.main_frame.winfo_children(): widget.destroy()
        
        ctk.CTkLabel(self.main_frame, text="Añadir Transacción", font=("Arial", 20)).pack(pady=20)
        
        self.entry_monto = ctk.CTkEntry(self.main_frame, placeholder_text="Monto", width=250)
        self.entry_monto.pack(pady=10)

        self.seg_tipo = ctk.CTkSegmentedButton(self.main_frame, values=["Ingreso", "Egreso"])
        self.seg_tipo.set("Egreso")
        self.seg_tipo.pack(pady=10)

        cuentas = [c[1] for c in logic.obtener_cuentas()]
        self.combo_cuenta = ctk.CTkComboBox(self.main_frame, values=cuentas, width=250)
        self.combo_cuenta.pack(pady=10)

        self.entry_cat = ctk.CTkEntry(self.main_frame, placeholder_text="Categoría (Ej: Alimentos)", width=250)
        self.entry_cat.pack(pady=10)

        self.entry_desc = ctk.CTkEntry(self.main_frame, placeholder_text="Mensaje (Opcional)", width=250) # [cite: 4]
        self.entry_desc.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Guardar", command=self.guardar).pack(pady=20)

    def guardar(self):
        try:
            monto = float(self.entry_monto.get())
            cuenta_nombre = self.combo_cuenta.get()
            cuenta_id = next(c[0] for c in logic.obtener_cuentas() if c[1] == cuenta_nombre)
            
            logic.registrar_movimiento(
                monto, self.seg_tipo.get(), cuenta_id, 
                self.entry_cat.get(), self.entry_desc.get() or None
            )
            messagebox.showinfo("Éxito", "Registrado correctamente")
            self.mostrar_resumen()
        except:
            messagebox.showerror("Error", "Datos inválidos")
        
    def mostrar_ventana_grafico(self):
        """Genera y muestra el gráfico en el panel principal."""
        if reports.generar_grafico_gastos():
            for w in self.main_frame.winfo_children(): w.destroy()
            
            # Cargamos la imagen generada
            img_reporte = ctk.CTkImage(light_image=Image.open("temp_reporte.png"),
                                      dark_image=Image.open("temp_reporte.png"),
                                      size=(500, 400))
            
            label_img = ctk.CTkLabel(self.main_frame, image=img_reporte, text="")
            label_img.pack(pady=20)
            
            ctk.CTkLabel(self.main_frame, text="Reporte Mensual Automático", font=("Arial", 18)).pack()
        else:
            messagebox.showwarning("Sin Datos", "Registra algunos gastos primero para generar el gráfico.")

if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()