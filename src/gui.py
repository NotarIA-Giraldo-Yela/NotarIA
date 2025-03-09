import tkinter as tk
from tkinter import Label, Button, filedialog
import cv2
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.scanner import scan_document
from scanner.scanner_doc import scan_doc
from image_processor import preprocess_image
from ocr.layoutlmv3_processor import process_document
from templates_handler.template_filler import update_docx_template
from templates_handler.form_filler import SaleDataApp


class NotarIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NotarIA - Lector de Documentos")
        self.root.geometry("900x750")

        # Variables para almacenar datos
        self.datos_comprador = None
        self.datos_vendedor = None
        self.datos_folio = None
        self.datos_manual = {}

        # Botón para escanear documento del comprador
        self.btn_escanear_comprador = Button(root, text="📑 Escanear Documento Comprador", command=self.buyer_info, width=25)
        self.btn_escanear_comprador.pack(pady=5)

        # Botón para escanear documento del vendedor
        self.btn_escanear_vendedor = Button(root, text="📑 Escanear Documento Vendedor", command=self.seller_info, width=25)
        self.btn_escanear_vendedor.pack(pady=5)

        # Botón para abrir el formulario de ingreso manual
        self.btn_ingreso_manual = Button(root, text="✍️ Ingreso Manual de Datos", command=self.manual_form, width=25)
        self.btn_ingreso_manual.pack(pady=5)

        # Botón para escanear Folio
        self.btn_cargar_folio = Button(root, text="📑 Escanear Folio ", command=self.folio_info, width=25)
        self.btn_cargar_folio.pack(pady=5)

        # Botón para generar la escritura
        self.btn_generar_escritura = Button(root, text="⚙️ Generar Escritura ", command=self.create_writing, width=25)
        self.btn_generar_escritura.pack(pady=5)

        # Etiqueta para mostrar resultados
        self.resultado_label = Label(root, text="🔍 Resultados aparecerán aquí", fg="blue", font=("Arial", 12), justify="left")
        self.resultado_label.pack(pady=10)

    def buyer_info(self):
        """ Escanea ambas caras del documento del comprador, guarda y muestra la información. """
        try:
            output_front = "scanned_front_comprador.png"
            output_back = "scanned_back_comprador.png"

            scan_document(output_front, output_back)

            processed_front = preprocess_image(cv2.imread(output_front))
            processed_back = preprocess_image(cv2.imread(output_back))

            cv2.imwrite(output_front, processed_front)
            cv2.imwrite(output_back, processed_back)

            self.datos_comprador = process_document(output_front, output_back)

            # Mostrar en pantalla
            self.mostrar_resultados("📌 **Datos del Comprador:**", self.datos_comprador)

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear el comprador: {str(e)}", fg="red")

    def seller_info(self):
        """ Escanea ambas caras del documento del vendedor, guarda y muestra la información. """
        try:
            output_front = "scanned_front_vendedor.png"
            output_back = "scanned_back_vendedor.png"

            scan_document(output_front, output_back)

            processed_front = preprocess_image(cv2.imread(output_front))
            processed_back = preprocess_image(cv2.imread(output_back))

            cv2.imwrite(output_front, processed_front)
            cv2.imwrite(output_back, processed_back)

            self.datos_vendedor = process_document(output_front, output_back)

            # Mostrar en pantalla
            self.mostrar_resultados("📌 **Datos del Vendedor:**", self.datos_vendedor)

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
            self.resultado_label.config(text=folio_texto, fg="blue")

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


    def mostrar_resultados(self, titulo, datos):
        """ Formatea y muestra los datos en la interfaz. """
        resultado_texto = f"{titulo}\n"
        resultado_texto += f"  - Número de Documento: {datos['Parte Frontal'].get('Número de Documento', 'No detectado')}\n"
        resultado_texto += f"  - Apellidos: {datos['Parte Frontal'].get('Apellidos', 'No detectado')}\n"
        resultado_texto += f"  - Nombres: {datos['Parte Frontal'].get('Nombres', 'No detectado')}\n\n"
        resultado_texto += f"📝 **Parte Trasera:**\n"
        resultado_texto += f"  - Fecha de nacimiento: {datos['Parte Trasera'].get('Fecha de nacimiento', 'No detectado')}\n"
        resultado_texto += f"  - Lugar de expedición: {datos['Parte Trasera'].get('Lugar de expedicion', 'No detectado')}\n"

        self.resultado_label.config(text=resultado_texto, fg="blue")

        


# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = NotarIAApp(root)
    root.mainloop()
