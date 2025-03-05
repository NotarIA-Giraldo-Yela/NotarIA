import tkinter as tk
from tkinter import filedialog, Label, Button
import cv2
from PIL import Image, ImageTk
import os
import uuid
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.scanner import scan_document
from scanner.scanner_doc import scan_doc
from image_processor import preprocess_image
from ocr.layoutlmv3_processor import process_document


class NotarIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NotarIA - Lector de Cédulas")
        self.root.geometry("900x750")

        # Botón para escanear documento del comprador
        self.btn_escanear = Button(root, text="📑 Escanear Documento Comprador", command=self.escanear_documento_comprador, width=25)
        self.btn_escanear.pack(pady=5)

        # Botón para escanear documento del vendedor
        self.btn_escanear = Button(root, text="📑 Escanear Documento Vendedor", command=self.escanear_documento_vendedor, width=25)
        self.btn_escanear.pack(pady=5)
        
        # Botón para escanear Folio
        self.btn_cargar = Button(root, text="📑 Escanear Folio ", command=self.escanear_folio, width=25)
        self.btn_cargar.pack(pady=5)

        # Botón para escanear foliop
        self.btn_cargar = Button(root, text="⚙️ Generar Escritura ", command=self.escanear_folio, width=25)
        self.btn_cargar.pack(pady=5)

        # Etiqueta para mostrar resultados
        self.resultado_label = Label(root, text="", fg="blue", font=("Arial", 12))
        self.resultado_label.pack(pady=10)

        self.imagen_front = None
        self.imagen_back = None
        self.imagen_actual = "front"  # Controla si se muestra la frontal o la trasera

    def escanear_documento_comprador(self):
        """ Escanea ambas caras del documento automáticamente a 600 ppp. """
        try:
            output_front = "scanned_front.png"
            output_back = "scanned_back.png"

            # Llamar al escaneo
            scan_document(output_front, output_back)

            self.imagen_front = output_front
            self.imagen_back = output_back
            self.imagen_actual = "front"
            
            processed_front = preprocess_image(cv2.imread(self.imagen_front))
            processed_back = preprocess_image(cv2.imread(self.imagen_back))

            self.imagen_front = "processed_front.png"
            self.imagen_back = "processed_back.png"

            cv2.imwrite(self.imagen_front, processed_front)
            cv2.imwrite(self.imagen_back, processed_back)

            datos_vendedor = process_document(self.imagen_front, self.imagen_back)
            datos_front_vendedor = datos_vendedor["Parte Frontal"]
            datos_back_vendedor = datos_vendedor["Parte Trasera"]

            resultado_texto = "📝 **Parte Frontal:**\n"
            resultado_texto += f"  Número de Documento: {datos_front_vendedor.get('Número de Documento', 'No detectado')}\n"
            resultado_texto += f"  Apellidos: {datos_front_vendedor.get('Apellidos', 'No detectado')}\n"
            resultado_texto += f"  Nombres: {datos_front_vendedor.get('Nombres', 'No detectado')}\n\n"

            resultado_texto += "📝 **Parte Trasera:**\n"
            resultado_texto += f"  Fecha de nacimiento: {datos_back_vendedor.get('Fecha de nacimiento', 'No detectado')}\n"
            resultado_texto += f"  Sexo: {datos_back_vendedor.get('Sexo', 'No detectado')}\n"
            resultado_texto += f"  Lugar de expedición: {datos_back_vendedor.get('Lugar de expedicion', 'No detectado')}\n"

            self.resultado_label.config(text=resultado_texto, fg="blue")

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear: {str(e)}", fg="red")



    def escanear_documento_vendedor(self):
        """ Escanea ambas caras del documento. """
        try:
            output_front = "scanned_front.png"
            output_back = "scanned_back.png"

            # Llamar al escaneo automático
            scan_document(output_front, output_back)

            self.imagen_front = output_front
            self.imagen_back = output_back
            self.imagen_actual = "front"

            self.mostrar_imagen(self.imagen_front)

            
            processed_front = preprocess_image(cv2.imread(self.imagen_front))
            processed_back = preprocess_image(cv2.imread(self.imagen_back))

            self.imagen_front = "processed_front.png"
            self.imagen_back = "processed_back.png"

            cv2.imwrite(self.imagen_front, processed_front)
            cv2.imwrite(self.imagen_back, processed_back)

            datos_comprador = process_document(self.imagen_front, self.imagen_back)
            datos_front_comprador = datos_comprador["Parte Frontal"]
            datos_back_comprador = datos_comprador["Parte Trasera"]

            resultado_texto = "📝 **Parte Frontal:**\n"
            resultado_texto += f"  Número de Documento: {datos_front_comprador.get('Número de Documento', 'No detectado')}\n"
            resultado_texto += f"  Apellidos: {datos_front_comprador.get('Apellidos', 'No detectado')}\n"
            resultado_texto += f"  Nombres: {datos_front_comprador.get('Nombres', 'No detectado')}\n\n"

            resultado_texto += "📝 **Parte Trasera:**\n"
            resultado_texto += f"  Fecha de nacimiento: {datos_back_comprador.get('Fecha de nacimiento', 'No detectado')}\n"
            resultado_texto += f"  Sexo: {datos_back_comprador.get('Sexo', 'No detectado')}\n"
            resultado_texto += f"  Lugar de expedición: {datos_back_comprador.get('Lugar de expedicion', 'No detectado')}\n"

            self.resultado_label.config(text=resultado_texto, fg="blue")

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear: {str(e)}", fg="red")


    def escanear_folio(self):
        """ Escanea folio de matricula. """
        try:
            output_doc = "Folio_Matricula"

            # Llamar al escaneo automático
            datos_folio = scan_doc(output_doc)
            
            matricula = datos_folio.get('matricula', 'No detectado')
            cedula_catastral = datos_folio.get('cedula_catastral', 'No detectado')
            ubicacion_predio = datos_folio.get('ubicacion_predio', 'No detectado')
            direccion_inmueble = datos_folio.get('direccion_inmueble', 'No detectado')

            self.imagen_doc = output_doc
            self.imagen_actual = "doc_fol"
            
            

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear: {str(e)}", fg="red")


    #def generar_escritura(self):



    def mostrar_imagen(self, path):
        """ Muestra la imagen en la interfaz gráfica. """
        img = Image.open(path)

        img = img.resize((400, 250))
        img_tk = ImageTk.PhotoImage(img)

        self.label_imagen.config(image=img_tk)
        self.label_imagen.image = img_tk

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = NotarIAApp(root)
    root.mainloop()
