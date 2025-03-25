import tkinter as tk
from tkinter import Label, Button, Toplevel, Entry
from tkinter import ttk
from tkinter import Label, Button, filedialog
import cv2
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.scanner import scan_document
from scanner.scanner_doc import scan_doc
from image_processor import preprocess_image
from ocr.doc_processor import process_document
from templates_handler.template_filler import update_docx_template
from templates_handler.form_filler import SaleDataApp
from PIL import Image, ImageTk  # Para cargar y mostrar el logo

class NotarIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NotarIA - Lector de Documentos")
        self.root.geometry("900x750")
        self.root.configure(bg="#254c9b")

        self.mostrando_datos = None

        # Inicializar los datos del comprador y vendedor
        self.datos_comprador = {
            "Parte Frontal": {
                "Número de Documento": "No detectado",
                "Apellidos": "No detectado",
                "Nombres": "No detectado"
            },
            "Parte Trasera": {
                "Lugar de Expedicion": "No detectado",
                "Fecha de Expedicion": "No detectado"
            }
        }

        self.datos_vendedor = {
            "Parte Frontal": {
                "Número de Documento": "No detectado",
                "Apellidos": "No detectado",
                "Nombres": "No detectado"
            },
            "Parte Trasera": {
                "Lugar de Expedicion": "No detectado",
                "Fecha de Expedicion": "No detectado"
            }
        }

        # Estilos para los botones
        style = ttk.Style()
        style.configure("Custom.TButton",
                        font=("Arial", 14, "bold"),
                        padding=10,
                        relief="flat",
                        background="#254c9b",
                        foreground="#254c9b",
                        borderwidth=0)

        style.map("Custom.TButton", 
                  background=[("active", "#e6791f"), ("!active", "#e6791f")],
                  foreground=[("active", "#000000"), ("!active", "#000000")])


        # Cargar y mostrar el logo
        logo_path = os.path.join(os.path.dirname(__file__), "data/Logo.png")
        if os.path.exists(logo_path):
            try:
                self.logo_image = Image.open(logo_path)
                self.logo_image = self.logo_image.resize((500, 265), Image.LANCZOS)  # Ajusta el tamaño según sea necesario
                self.logo_photo = ImageTk.PhotoImage(self.logo_image)
                self.logo_label = Label(root, image=self.logo_photo, bg="#254c9b")
                self.logo_label.pack(pady=(5))
            except Exception as e:
                print(f"Error al cargar la imagen del logo: {e}")
        else:
            print(f"⚠️ Advertencia: La imagen del logo no se encontró en la ruta: {logo_path}")
        
        # Contenedor principal centrado
        frame = tk.Frame(root, bg="#254c9b")
        frame.pack(pady=5)


        # Botones con estilos mejorados
        self.btn_escanear_comprador = ttk.Button(frame, text="📑 Escanear Documento Comprador", 
                                                 command=self.buyer_info, 
                                                 style="Custom.TButton")
        self.btn_escanear_comprador.pack(pady=10, ipadx=20, ipady=5)

        self.btn_escanear_vendedor = ttk.Button(frame, text="📑 Escanear Documento Vendedor", 
                                                command=self.seller_info, 
                                                style="Custom.TButton")
        self.btn_escanear_vendedor.pack(pady=10, ipadx=20, ipady=5)

        self.btn_ingreso_manual = ttk.Button(frame, text="✍️ Ingreso Manual de Datos", 
                                             command=self.manual_form, 
                                             style="Custom.TButton")
        self.btn_ingreso_manual.pack(pady=10, ipadx=20, ipady=5)

        self.btn_cargar_folio = ttk.Button(frame, text="📑 Escanear Folio", 
                                           command=self.folio_info, 
                                           style="Custom.TButton")
        self.btn_cargar_folio.pack(pady=10, ipadx=20, ipady=5)

        self.btn_generar_escritura = ttk.Button(frame, text="⚙️ Generar Escritura", 
                                                command=self.create_writing, 
                                                style="Custom.TButton")
        self.btn_generar_escritura.pack(pady=10, ipadx=20, ipady=5)

        # Etiqueta de resultados
        self.resultado_label = Label(root, text="🔍 Resultados aparecerán aquí", fg="orange", 
                                    font=("Arial", 20), bg="#254c9b")
        self.resultado_label.pack(pady=5)

        # Botón "Corregir Datos"
        self.btn_correccion = ttk.Button(root, text="✏️ Corregir Datos", command=self.open_edit, style="Custom.TButton")
        self.btn_correccion.pack(pady=10)
        self.btn_correccion.pack_forget()  # Inicialmente oculto
    

    def buyer_info(self):
        """ Escanea ambas caras del documento del comprador, guarda y muestra la información. """
        try:
            output_front = "scanned_front_comprador.png"
            output_back = "scanned_back_comprador.png"

            scan_document(output_front, output_back)

            self.datos_comprador = process_document(output_front, output_back)

            # Mostrar en pantalla
            self.mostrar_resultados("📌 Datos del Comprador:", self.datos_comprador, "comprador")

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear el comprador: {str(e)}", fg="red")

    def seller_info(self):
        """ Escanea ambas caras del documento del vendedor, guarda y muestra la información. """
        try:
            output_front = "scanned_front_vendedor.png"
            output_back = "scanned_back_vendedor.png"

            scan_document(output_front, output_back)
      
            self.datos_vendedor = process_document(output_front, output_back)

            # Mostrar en pantalla
            self.mostrar_resultados("📌 Datos del Vendedor:", self.datos_vendedor, "vendedor")

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear el vendedor: {str(e)}", fg="red")

    def manual_form(self):
        """ Abre el formulario de ingreso manual de datos y recupera la información. """
        manual_root = tk.Toplevel(self.root)
        app = SaleDataApp(manual_root)
        manual_root.wait_window()  # Espera a que el usuario cierre la ventana
    
        # Recuperar los datos ingresados manualmente
        self.datos_manual = app.data
        print("Datos manuales ingresados:", self.datos_manual)  # Depuración

    def folio_info(self):
        """ Escanea folio de matrícula y guarda la información. """
        try:
            output_doc = "Folio_Matricula"

            self.datos_folio = scan_doc(output_doc)

            # Mostrar resultados en pantalla
            folio_texto = f"""
            📌 **Datos del Folio:**
            - Matrícula: {self.datos_folio.get('matricula', 'No detectado')}
            - Cédula Catastral: {self.datos_folio.get('cedula_catastral', 'No detectado')}
            - Ubicación: {self.datos_folio.get('ubicacion_predio', 'No detectado')}
            - Dirección: {self.datos_folio.get('direccion_inmueble', 'No detectado')}
            """
            self.resultado_label.config(text=folio_texto, fg="white")

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear folio: {str(e)}", fg="red")

    def create_writing(self):
        """ Genera la escritura con los datos escaneados. Indica si falta algún documento. """
        faltantes = []

        if not self.datos_comprador:
            faltantes.append("Documento del Comprador")
        if not self.datos_vendedor:
            faltantes.append("Documento del Vendedor")
        if not self.datos_folio:
            faltantes.append("Folio de Matrícula")

        if not self.datos_comprador and "comprador" not in self.datos_manual:
            faltantes.append("Datos del comprador")

        if not self.datos_vendedor and "vendedor" not in self.datos_manual:
            faltantes.append("Datos del vendedor")

        if faltantes:
            mensaje_error = f"⚠️ Error: Faltan los siguientes documentos:\n" + "\n".join(f"- {doc}" for doc in faltantes)
            self.resultado_label.config(text=mensaje_error, fg="red")
            return

        escritura = f"""
        📝 **Escritura de Compraventa**
    
        👤 **Comprador:**
        - Nombre: {self.datos_comprador['Parte Frontal'].get('Nombres', 'No detectado')} {self.datos_comprador['Parte Frontal'].get('Apellidos', 'No detectado')}
        - Documento: {self.datos_comprador['Parte Frontal'].get('Número de Documento', 'No detectado')}
        - Lugar de Expedición: {self.datos_comprador['Parte Trasera'].get('Lugar de expedicion', 'No detectado')}
        - Afectación: {self.datos_manual['comprador'].get('afectacion', 'No ingresado')}
        - Estado Civil: {self.datos_manual['comprador'].get('estadoCivil', 'No ingresado')}
        - Sociedad:{self.datos_manual['comprador'].get('sociedad', 'No ingresado')}
        - Dirección:{self.datos_manual['comprador'].get('direccion', 'No ingresado')}
        - Correo Electronico:{self.datos_manual['comprador'].get('correo', 'No ingresado')}
        - Teléfono Celular: {self.datos_manual['comprador'].get('telefonoCel', 'No ingresado')}
        - Telefono Fijo: {self.datos_manual['comprador'].get('telefonoFijo', 'No ingresado')}
    
        👤 **Vendedor:**
        - Nombre: {self.datos_vendedor['Parte Frontal'].get('Nombres', 'No detectado')} {self.datos_vendedor['Parte Frontal'].get('Apellidos', 'No detectado')}
        - Documento: {self.datos_vendedor['Parte Frontal'].get('Número de Documento', 'No detectado')}
        - Lugar de Expedición: {self.datos_vendedor['Parte Trasera'].get('Lugar de expedicion', 'No detectado')}
        - Afectación: {self.datos_manual['vendedor'].get('afectacion', 'No ingresado')}
        - Estado Civil: {self.datos_manual['vendedor'].get('estadoCivil', 'No ingresado')}
        - Sociedad:{self.datos_manual['vendedor'].get('sociedad', 'No ingresado')}
        - Dirección:{self.datos_manual['vendedor'].get('direccion', 'No ingresado')}
        - Correo Electronico:{self.datos_manual['vendedor'].get('correo', 'No ingresado')}
        - Teléfono Celular: {self.datos_manual['vendedor'].get('telefonoCel', 'No ingresado')}
        - Telefono Fijo: {self.datos_manual['vendedor'].get('telefonoFijo', 'No ingresado')}
    
        🏠 **Datos del Inmueble:**
        - Valor de la Venta: {self.datos_manual.get('valorVenta', 'No ingresado')}
        - Matrícula: {self.datos_folio.get('matricula', 'No detectado')}
        - Cédula Catastral: {self.datos_folio.get('cedula_catastral', 'No detectado')}
        - Ubicación: {self.datos_folio.get('ubicacion_predio', 'No detectado')}
        - Dirección: {self.datos_folio.get('direccion_inmueble', 'No detectado')}
        """

        # Guardar la escritura en un archivo
        with open("escritura.txt", "w", encoding="utf-8") as file:
            file.write(escritura)

        # Ahora, solicitar la plantilla DOCX para insertar los datos extraídos
        docx_path = filedialog.askopenfilename(
            title="Selecciona la plantilla DOCX",
            filetypes=[("Documentos DOCX", "*.docx")]
        )
        
        if docx_path:
            extracted_data = {
                "nombre_comprador": self.datos_comprador['Parte Frontal'].get('Apellidos', 'No detectado')  + " " + self.datos_comprador['Parte Frontal'].get('Nombres', 'No detectado'),
                "apellidos_comprador": self.datos_comprador['Parte Frontal'].get('Apellidos', 'No detectado'),
                "num_doc_comprador": self.datos_comprador['Parte Frontal'].get('Número de Documento', 'No detectado'),
                "lugar_expe_comprador": self.datos_comprador['Parte Trasera'].get('Lugar de expedicion', 'No detectado'),
                "afectacion_comprador": {self.datos_manual['comprador'].get('afectacion', 'No ingresado')},
                "estadoCivil_comprador": {self.datos_manual['comprador'].get('estadoCivil', 'No ingresado')},
                "sociedad_comprador":{self.datos_manual['comprador'].get('sociedad', 'No ingresado')},
                "direccion_comprador":{self.datos_manual['comprador'].get('direccion', 'No ingresado')},
                "correo_comprador":{self.datos_manual['comprador'].get('correo', 'No ingresado')},
                "telefonoCel_comprador": {self.datos_manual['comprador'].get('telefonoCel', 'No ingresado')},
                "telefonoFijo_comprador": {self.datos_manual['comprador'].get('telefonoFijo', 'No ingresado')},

                "nombre_vendedor": self.datos_vendedor['Parte Frontal'].get('Nombres', 'No detectado') + " " + self.datos_vendedor['Parte Frontal'].get('Apellidos', 'No detectado'),
                "apellidos_vendedor": self.datos_vendedor['Parte Frontal'].get('Apellidos', 'No detectado'),
                "num_doc_vendedor": self.datos_vendedor['Parte Frontal'].get('Número de Documento', 'No detectado'),
                "lugar_expe_vendedor": self.datos_vendedor['Parte Trasera'].get('Lugar de expedicion', 'No detectado'),
                "afectacion_vendedor": {self.datos_manual['vendedor'].get('afectacion', 'No ingresado')},
                "estadoCivil_vendedor": {self.datos_manual['vendedor'].get('estadoCivil', 'No ingresado')},
                "sociedad_vendedor":{self.datos_manual['vendedor'].get('sociedad', 'No ingresado')},
                "direccion_vendedor":{self.datos_manual['vendedor'].get('direccion', 'No ingresado')},
                "correo_vendedor":{self.datos_manual['vendedor'].get('correo', 'No ingresado')},
                "telefonoCel_vendedor": {self.datos_manual['vendedor'].get('telefonoCel', 'No ingresado')},
                "telefonoFijo_vendedor": {self.datos_manual['vendedor'].get('telefonoFijo', 'No ingresado')},

                "valorVenta": {self.datos_manual.get('valorVenta', 'No ingresado')},
                "matricula": self.datos_folio.get('matricula', 'No detectado'),
                "cedula_catastral": self.datos_folio.get('cedula_catastral', 'No detectado'),
                "ubicacion_predio": self.datos_folio.get('ubicacion_predio', 'No detectado'),
                "direccion_inmueble": self.datos_folio.get('direccion_inmueble', 'No detectado')
            }
            output_docx = "Documento_Actualizado.docx"
            update_docx_template(docx_path, output_docx, extracted_data)
        
        self.resultado_label.config(text="✅ Escritura generada correctamente. Guardada como 'escritura.txt'", fg="green")


    def mostrar_resultados(self, titulo, datos, tipo):
        """ Formatea y muestra los datos en la interfaz. """
        
        self.mostrando_datos = tipo
        resultado_texto = f"{titulo}\n"
        resultado_texto += f"  - Número de Documento: {datos['Parte Frontal'].get('Número de Documento', 'No detectado')}\n"
        resultado_texto += f"  - Apellidos: {datos['Parte Frontal'].get('Apellidos', 'No detectado')}\n"
        resultado_texto += f"  - Nombres: {datos['Parte Frontal'].get('Nombres', 'No detectado')}\n"
        resultado_texto += f"  - Lugar de expedición: {datos['Parte Trasera'].get('Lugar de Expedicion', 'No detectado')}\n"
        resultado_texto += f"  - Fecha de Expedición: {datos['Parte Trasera'].get('Fecha de Expedicion', 'No detectado')}\n"

        # Actualizar el texto en la etiqueta de resultados
        self.resultado_label.config(text=resultado_texto, fg="white", bg="#254c9b", font=("Arial", 14, "bold"))

        # Mostrar el botón "Corregir Datos" debajo de los resultados
        self.btn_correccion.pack(pady=10)

    def open_edit(self):
        """ Abre una ventana para editar los datos mostrados """
        if not self.mostrando_datos:
            return  # Si no hay datos mostrados, no abrir la ventana

        # Crear la ventana de edición y guardar la referencia
        self.edicion_root = Toplevel(self.root)
        self.edicion_root.title("Editar Datos")
        self.edicion_root.geometry("400x400")  # Ajustar el tamaño para incluir todos los campos

        # Título de la ventana
        Label(self.edicion_root, text=f"Editar Datos del {self.mostrando_datos.capitalize()}").pack(pady=10)

        # Obtener los datos actuales (comprador o vendedor)
        if self.mostrando_datos == "comprador":
            datos_actuales = self.datos_comprador
        else:
            datos_actuales = self.datos_vendedor

        # Diccionario para almacenar las referencias a los campos de texto (Entry)
        self.entries_edicion = {}

        # Campos a editar y su ubicación en la estructura de datos
        campos = [
            ("Número de Documento", "Parte Frontal"),
            ("Apellidos", "Parte Frontal"),
            ("Nombres", "Parte Frontal"),
            ("Lugar de Expedicion", "Parte Trasera"),
            ("Fecha de Expedicion", "Parte Trasera")  # Añadimos el campo "Fecha de Expedicion"
        ]

        # Crear y prellenar los campos de texto
        for key, seccion in campos:
            # Etiqueta del campo
            Label(self.edicion_root, text=key).pack(pady=5)

            # Campo de texto (Entry)
            entry = Entry(self.edicion_root, width=30)
            
            # Prellenar el campo con el valor actual si existe
            if key in datos_actuales[seccion]:
                entry.insert(0, datos_actuales[seccion][key])
            else:
                entry.insert(0, "No detectado")  # Si no hay datos, mostrar "No detectado"
            
            entry.pack(pady=5)
            self.entries_edicion[key] = entry  # Guardar referencia al campo

        # Botón para guardar los cambios
        Button(self.edicion_root, text="Guardar Cambios", command=self.save_edit).pack(pady=20)

    def save_edit(self):
        """ Guarda los cambios realizados en la ventana de edición """
        if self.mostrando_datos == "comprador":
            datos_actuales = self.datos_comprador
        else:
            datos_actuales = self.datos_vendedor

        for key, entry in self.entries_edicion.items():
            # Determinar en qué parte del diccionario se debe guardar el valor
            if key in ["Número de Documento", "Apellidos", "Nombres"]:
                datos_actuales["Parte Frontal"][key] = entry.get()
            elif key in ["Lugar de Expedicion", "Fecha de Expedicion"]:
                datos_actuales["Parte Trasera"][key] = entry.get()
        
        if self.mostrando_datos == "comprador":
            self.datos_comprador = datos_actuales
        else:
            self.datos_vendedor = datos_actuales

        # Cerrar la ventana de edición
        self.edicion_root.destroy()

        # Mostrar los resultados actualizados
        if self.mostrando_datos == "comprador":
            self.mostrar_resultados("📌 Datos del Comprador:", self.datos_comprador, "comprador")
        else:
            self.mostrar_resultados("📌 Datos del Vendedor:", self.datos_vendedor, "vendedor")
        

        


# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = NotarIAApp(root)
    root.mainloop()
