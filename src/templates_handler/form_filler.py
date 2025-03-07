import tkinter as tk
from tkinter import ttk, messagebox
from num2words import num2words


class SaleDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingreso de Datos de Venta")
        self.data = {}
        
        # Crear frames para cada etapa
        self.frame_initial = tk.Frame(root)
        self.frame_seller = tk.Frame(root)
        self.frame_buyer = tk.Frame(root)
        self.frame_result = tk.Frame(root)
        
        self.setup_initial_frame()
        self.setup_seller_frame()
        self.setup_buyer_frame()
        self.setup_result_frame()
        
        self.frame_initial.pack(padx=10, pady=10)
        
    def setup_initial_frame(self):
        # Valor de la venta (entero) con puntos permitidos y conversión a letras
        tk.Label(self.frame_initial, text="Valor de la Venta (entero):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_sale = tk.Entry(self.frame_initial)
        self.entry_sale.grid(row=0, column=1, padx=5, pady=5)
        # Actualiza la conversión a letras en cada cambio
        self.entry_sale.bind("<KeyRelease>", self.update_letras)
        
        tk.Label(self.frame_initial, text="Valor en letras:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.label_letras = tk.Label(self.frame_initial, text="", fg="blue")
        self.label_letras.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Selección entre Vendedor o Comprador
        tk.Label(self.frame_initial, text="Seleccione los datos a ingresar:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.tipo_var = tk.StringVar(value="vendedor")
        tk.Radiobutton(self.frame_initial, text="Vendedor", variable=self.tipo_var, value="vendedor").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        tk.Radiobutton(self.frame_initial, text="Comprador", variable=self.tipo_var, value="comprador").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        tk.Button(self.frame_initial, text="Siguiente", command=self.initial_next).grid(row=3, column=0, columnspan=3, pady=10)
        
    def update_letras(self, event=None):
        # Elimina los puntos y convierte el número a entero para pasarlo a num2words.
        valor = self.entry_sale.get().replace(".", "")
        try:
            number = int(valor)
            # Convierte a letras y pasa a mayúsculas.
            letras = num2words(number, lang='es').upper()
            self.label_letras.config(text=letras)
        except ValueError:
            self.label_letras.config(text="")
    
    def initial_next(self):
        sale_value_str = self.entry_sale.get()
        try:
            # Elimina los puntos antes de la conversión
            sale_value = int(sale_value_str.replace(".", ""))
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor entero válido para la venta. Use puntos como separadores de miles si es necesario.")
            return
        self.data["valorVenta"] = sale_value
        
        tipo = self.tipo_var.get()
        self.data["tipoIngreso"] = tipo
        
        self.frame_initial.pack_forget()
        if tipo == "vendedor":
            self.prefill_seller()  # Prellenar si existen datos previos
            self.frame_seller.pack(padx=10, pady=10)
        else:
            self.prefill_buyer()  # Prellenar si existen datos previos
            self.frame_buyer.pack(padx=10, pady=10)
    
    def setup_seller_frame(self):
        tk.Label(self.frame_seller, text="Datos del VENDEDOR", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Afectación a Vivienda Familiar
        tk.Label(self.frame_seller, text="Afectación a Vivienda Familiar:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.seller_afectacion_var = tk.StringVar()
        self.seller_afectacion_menu = ttk.Combobox(self.frame_seller, textvariable=self.seller_afectacion_var, state="readonly")
        self.seller_afectacion_menu['values'] = ("SI", "NO")
        self.seller_afectacion_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Estado Civil
        tk.Label(self.frame_seller, text="Estado Civil:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.seller_estado_var = tk.StringVar()
        self.seller_estado_menu = ttk.Combobox(self.frame_seller, textvariable=self.seller_estado_var, state="readonly")
        self.seller_estado_menu['values'] = ("SOLTERO", "CASADO", "DIVORICIADO", "VIUDO", "UNION MARITAL DE HECHO")
        self.seller_estado_menu.grid(row=2, column=1, padx=5, pady=5)
        
        # Sociedad Conyugal Vigente
        tk.Label(self.frame_seller, text="Sociedad Conyugal Vigente:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.seller_sociedad_var = tk.StringVar()
        self.seller_sociedad_menu = ttk.Combobox(self.frame_seller, textvariable=self.seller_sociedad_var, state="readonly")
        self.seller_sociedad_menu['values'] = ("SIN", "CON")
        self.seller_sociedad_menu.grid(row=3, column=1, padx=5, pady=5)
        
        # Dirección Residencia
        tk.Label(self.frame_seller, text="Dirección Residencia:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.seller_direccion = tk.Entry(self.frame_seller)
        self.seller_direccion.grid(row=4, column=1, padx=5, pady=5)
        
        # Correo Electrónico
        tk.Label(self.frame_seller, text="Correo Electrónico:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.seller_correo = tk.Entry(self.frame_seller)
        self.seller_correo.grid(row=5, column=1, padx=5, pady=5)
        
        # Teléfono Cel
        tk.Label(self.frame_seller, text="Teléfono Cel:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.seller_tel_cel = tk.Entry(self.frame_seller)
        self.seller_tel_cel.grid(row=6, column=1, padx=5, pady=5)
        
        # Teléfono Fijo
        tk.Label(self.frame_seller, text="Teléfono Fijo:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.seller_tel_fijo = tk.Entry(self.frame_seller)
        self.seller_tel_fijo.grid(row=7, column=1, padx=5, pady=5)
        
        # Botón para pasar a datos del comprador
        tk.Button(self.frame_seller, text="Siguiente: Datos del Comprador", command=self.seller_next).grid(row=8, column=0, columnspan=2, pady=10)
    
    def seller_next(self):
        # Validación de campos del VENDEDOR
        if (not self.seller_afectacion_var.get() or not self.seller_estado_var.get() or not self.seller_sociedad_var.get() or
            not self.seller_direccion.get() or not self.seller_correo.get() or not self.seller_tel_cel.get() or not self.seller_tel_fijo.get()):
            messagebox.showerror("Error", "Por favor, complete todos los datos del VENDEDOR.")
            return
        # Guardar datos del VENDEDOR
        self.data["vendedor"] = {
            "afectacion": self.seller_afectacion_var.get(),
            "estadoCivil": self.seller_estado_var.get(),
            "sociedad": self.seller_sociedad_var.get(),
            "direccion": self.seller_direccion.get(),
            "correo": self.seller_correo.get(),
            "telefonoCel": self.seller_tel_cel.get(),
            "telefonoFijo": self.seller_tel_fijo.get()
        }
        self.frame_seller.pack_forget()
        self.prefill_buyer()  # Prellenar datos del comprador si existen
        self.frame_buyer.pack(padx=10, pady=10)
    
    def setup_buyer_frame(self):
        tk.Label(self.frame_buyer, text="Datos del COMPRADOR", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Afectación a Vivienda Familiar
        tk.Label(self.frame_buyer, text="Afectación a Vivienda Familiar:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.buyer_afectacion_var = tk.StringVar()
        self.buyer_afectacion_menu = ttk.Combobox(self.frame_buyer, textvariable=self.buyer_afectacion_var, state="readonly")
        self.buyer_afectacion_menu['values'] = ("SI", "NO")
        self.buyer_afectacion_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Estado Civil
        tk.Label(self.frame_buyer, text="Estado Civil:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.buyer_estado_var = tk.StringVar()
        self.buyer_estado_menu = ttk.Combobox(self.frame_buyer, textvariable=self.buyer_estado_var, state="readonly")
        self.buyer_estado_menu['values'] = ("SOLTERO", "CASADO", "DIVORCIADO", "VIUDO", "UNION MARITAL DE HECHO")
        self.buyer_estado_menu.grid(row=2, column=1, padx=5, pady=5)
        
        # Sociedad Conyugal Vigente
        tk.Label(self.frame_buyer, text="Sociedad Conyugal Vigente:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.buyer_sociedad_var = tk.StringVar()
        self.buyer_sociedad_menu = ttk.Combobox(self.frame_buyer, textvariable=self.buyer_sociedad_var, state="readonly")
        self.buyer_sociedad_menu['values'] = ("SIN", "CON")
        self.buyer_sociedad_menu.grid(row=3, column=1, padx=5, pady=5)
        
        # Dirección Residencia
        tk.Label(self.frame_buyer, text="Dirección Residencia:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.buyer_direccion = tk.Entry(self.frame_buyer)
        self.buyer_direccion.grid(row=4, column=1, padx=5, pady=5)
        
        # Correo Electrónico
        tk.Label(self.frame_buyer, text="Correo Electrónico:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.buyer_correo = tk.Entry(self.frame_buyer)
        self.buyer_correo.grid(row=5, column=1, padx=5, pady=5)
        
        # Teléfono Cel
        tk.Label(self.frame_buyer, text="Teléfono Cel:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.buyer_tel_cel = tk.Entry(self.frame_buyer)
        self.buyer_tel_cel.grid(row=6, column=1, padx=5, pady=5)
        
        # Teléfono Fijo
        tk.Label(self.frame_buyer, text="Teléfono Fijo:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.buyer_tel_fijo = tk.Entry(self.frame_buyer)
        self.buyer_tel_fijo.grid(row=7, column=1, padx=5, pady=5)
        
        # Botón para enviar los datos
        tk.Button(self.frame_buyer, text="Enviar Datos", command=self.submit).grid(row=8, column=0, columnspan=2, pady=10)
    
    def setup_result_frame(self):
        # Frame de resultados
        self.result_label = tk.Label(self.frame_result, text="", justify="left", font=("Courier", 10))
        self.result_label.pack(padx=10, pady=10)
        # Botones para guardar y corregir
        button_frame = tk.Frame(self.frame_result)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Guardar y Cerrar", command=self.cerrar_y_guardar).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Corregir", command=self.correct_data).grid(row=0, column=1, padx=5)
    
    def submit(self):
        # Validación de campos del COMPRADOR
        if (not self.buyer_afectacion_var.get() or not self.buyer_estado_var.get() or not self.buyer_sociedad_var.get() or
            not self.buyer_direccion.get() or not self.buyer_correo.get() or not self.buyer_tel_cel.get() or not self.buyer_tel_fijo.get()):
            messagebox.showerror("Error", "Por favor, complete todos los datos del COMPRADOR.")
            return
        
        self.data["comprador"] = {
            "afectacion": self.buyer_afectacion_var.get(),
            "estadoCivil": self.buyer_estado_var.get(),
            "sociedad": self.buyer_sociedad_var.get(),
            "direccion": self.buyer_direccion.get(),
            "correo": self.buyer_correo.get(),
            "telefonoCel": self.buyer_tel_cel.get(),
            "telefonoFijo": self.buyer_tel_fijo.get()
        }
        self.frame_buyer.pack_forget()
        self.show_results()
    
    def show_results(self):
    # Convertir el valor de la venta a letras
        valor_venta_letras = num2words(self.data["valorVenta"], lang='es').upper()
        result_str = f"Valor de la Venta: {self.data['valorVenta']}\n ({valor_venta_letras})\n"
        result_str += "-" * 40 + "\n"
        if "vendedor" in self.data:
            result_str += "Datos del VENDEDOR:\n"
            result_str += f"  Afectación a Vivienda Familiar: {self.data['vendedor']['afectacion']}\n"
            result_str += f"  Estado Civil: {self.data['vendedor']['estadoCivil']}\n"
            result_str += f"  Sociedad Conyugal Vigente: {self.data['vendedor']['sociedad']}\n"
            result_str += f"  Dirección Residencia: {self.data['vendedor']['direccion']}\n"
            result_str += f"  Correo Electrónico: {self.data['vendedor']['correo']}\n"
            result_str += f"  Teléfono Cel: {self.data['vendedor']['telefonoCel']}\n"
            result_str += f"  Teléfono Fijo: {self.data['vendedor']['telefonoFijo']}\n"
            result_str += "-" * 40 + "\n"
        if "comprador" in self.data:
            result_str += "Datos del COMPRADOR:\n"
            result_str += f"  Afectación a Vivienda Familiar: {self.data['comprador']['afectacion']}\n"
            result_str += f"  Estado Civil: {self.data['comprador']['estadoCivil']}\n"
            result_str += f"  Sociedad Conyugal Vigente: {self.data['comprador']['sociedad']}\n"
            result_str += f"  Dirección Residencia: {self.data['comprador']['direccion']}\n"
            result_str += f"  Correo Electrónico: {self.data['comprador']['correo']}\n"
            result_str += f"  Teléfono Cel: {self.data['comprador']['telefonoCel']}\n"
            result_str += f"  Teléfono Fijo: {self.data['comprador']['telefonoFijo']}\n"
            result_str += "-" * 40 + "\n"
    
        self.result_label.config(text=result_str)
        self.frame_result.pack(padx=10, pady=10)

    
    def correct_data(self):
        # Crear ventana de corrección
        self.correction_window = tk.Toplevel(self.root)
        self.correction_window.title("Corregir Datos")
        tk.Label(self.correction_window, text="¿Qué desea corregir?").pack(padx=10, pady=10)
        
        self.correction_var = tk.StringVar(value="venta")
        # Opciones: "venta", "vendedor", "comprador"
        tk.Radiobutton(self.correction_window, text="Valor de la Venta", variable=self.correction_var, value="venta").pack(anchor="w", padx=10)
        tk.Radiobutton(self.correction_window, text="Datos del VENDEDOR", variable=self.correction_var, value="vendedor").pack(anchor="w", padx=10)
        tk.Radiobutton(self.correction_window, text="Datos del COMPRADOR", variable=self.correction_var, value="comprador").pack(anchor="w", padx=10)
        
        tk.Button(self.correction_window, text="Aceptar", command=self.apply_correction).pack(pady=10)
    
    def apply_correction(self):
        option = self.correction_var.get()
        self.correction_window.destroy()
        self.frame_result.pack_forget()  # Oculta la pantalla de resultados
        if option == "venta":
            self.prefill_initial()
            self.frame_initial.pack(padx=10, pady=10)
        elif option == "vendedor":
            self.prefill_seller()
            self.frame_seller.pack(padx=10, pady=10)
        elif option == "comprador":
            self.prefill_buyer()
            self.frame_buyer.pack(padx=10, pady=10)
    
    def prefill_initial(self):
        self.entry_sale.delete(0, tk.END)
        self.entry_sale.insert(0, str(self.data.get("valorVenta", "")))
        # Actualiza la conversión a letras
        self.update_letras()
        tipo = self.data.get("tipoIngreso", "vendedor")
        self.tipo_var.set(tipo)
    
    def prefill_seller(self):
        if "vendedor" in self.data:
            self.seller_afectacion_var.set(self.data["vendedor"].get("afectacion", ""))
            self.seller_estado_var.set(self.data["vendedor"].get("estadoCivil", ""))
            self.seller_sociedad_var.set(self.data["vendedor"].get("sociedad", ""))
            self.seller_direccion.delete(0, tk.END)
            self.seller_direccion.insert(0, self.data["vendedor"].get("direccion", ""))
            self.seller_correo.delete(0, tk.END)
            self.seller_correo.insert(0, self.data["vendedor"].get("correo", ""))
            self.seller_tel_cel.delete(0, tk.END)
            self.seller_tel_cel.insert(0, self.data["vendedor"].get("telefonoCel", ""))
            self.seller_tel_fijo.delete(0, tk.END)
            self.seller_tel_fijo.insert(0, self.data["vendedor"].get("telefonoFijo", ""))
    
    def prefill_buyer(self):
        if "comprador" in self.data:
            self.buyer_afectacion_var.set(self.data["comprador"].get("afectacion", ""))
            self.buyer_estado_var.set(self.data["comprador"].get("estadoCivil", ""))
            self.buyer_sociedad_var.set(self.data["comprador"].get("sociedad", ""))
            self.buyer_direccion.delete(0, tk.END)
            self.buyer_direccion.insert(0, self.data["comprador"].get("direccion", ""))
            self.buyer_correo.delete(0, tk.END)
            self.buyer_correo.insert(0, self.data["comprador"].get("correo", ""))
            self.buyer_tel_cel.delete(0, tk.END)
            self.buyer_tel_cel.insert(0, self.data["comprador"].get("telefonoCel", ""))
            self.buyer_tel_fijo.delete(0, tk.END)
            self.buyer_tel_fijo.insert(0, self.data["comprador"].get("telefonoFijo", ""))
    
    def cerrar_y_guardar(self):
        """ Guarda los datos ingresados y cierra la ventana. """
        if not self.data:
            messagebox.showwarning("Advertencia", "No hay datos ingresados.")
            return
        self.root.destroy()  # Cierra la ventana

if __name__ == "__main__":
    root = tk.Tk()
    app = SaleDataApp(root)
    root.mainloop()

