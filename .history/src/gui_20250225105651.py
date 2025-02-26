import tkinter as tk
from tkinter import filedialog, Label, Button
import cv2
from PIL import Image, ImageTk
import os
import uuid
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.scanner import scan_document
from image_processor import preprocess_image
from ocr.layoutlmv3_processor import process_document


from src.scanner.scanner import scan_document
from src.image_processor import preprocess_image
from src.ocr.layoutlmv3_processor import process_document

class NotarIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NotarIA - Lector de Cédulas")
        self.root.geometry("900x750")

        # Botón para escanear documento
        self.btn_escanear = Button(root, text="📑 Escanear Documento", command=self.escanear_documento, width=25)
        self.btn_escanear.pack(pady=5)

        # Botón para cargar imagen manualmente
        self.btn_cargar = Button(root, text="📂 Cargar Imágenes", command=self.cargar_imagen, width=25)
        self.btn_cargar.pack(pady=5)

        # Mostrar imagen escaneada
        self.label_imagen = Label(root)
        self.label_imagen.pack()

        # Botón para alternar entre imágenes frontal y trasera
        self.btn_cambiar_imagen = Button(root, text="🔄 Alternar Imagen", command=self.cambiar_imagen, width=25)
        self.btn_cambiar_imagen.pack(pady=5)

        # Botón para procesar imagen
        self.btn_procesar = Button(root, text="⚙️ Preprocesar Imagen", command=self.preprocesar_imagen, width=25)
        self.btn_procesar.pack(pady=5)

        # Botón para ejecutar OCR
        self.btn_ocr = Button(root, text="🔍 Extraer Datos", command=self.ejecutar_ocr, width=25)
        self.btn_ocr.pack(pady=5)

        # Etiqueta para mostrar resultados
        self.resultado_label = Label(root, text="", fg="blue", font=("Arial", 12))
        self.resultado_label.pack(pady=10)

        self.imagen_front = None
        self.imagen_back = None
        self.imagen_actual = "front"  # Controla si se muestra la frontal o la trasera

    def escanear_documento(self):
        """ Escanea ambas caras del documento automáticamente a 600 ppp. """
        try:
            output_front = "scanned_front.png"
            output_back = "scanned_back.png"

            # Llamar al escaneo automático
            scan_document(output_front, output_back)

            self.imagen_front = output_front
            self.imagen_back = output_back
            self.imagen_actual = "front"

            self.mostrar_imagen(self.imagen_front)
            self.resultado_label.config(text="✅ Documento escaneado correctamente a 600 ppp.", fg="green")

        except Exception as e:
            self.resultado_label.config(text=f"⚠️ Error al escanear: {str(e)}", fg="red")

    def cargar_imagen(self):
        """ Permite seleccionar las imágenes frontal y trasera manualmente. """
        file_path_front = filedialog.askopenfilename(title="Selecciona la imagen frontal", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path_front:
            self.imagen_front = file_path_front

        file_path_back = filedialog.askopenfilename(title="Selecciona la imagen trasera", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path_back:
            self.imagen_back = file_path_back

        self.imagen_actual = "front"
        self.mostrar_imagen(self.imagen_front)

    def cambiar_imagen(self):
        """ Alterna entre la imagen frontal y trasera. """
        if self.imagen_front and self.imagen_back:
            if self.imagen_actual == "front":
                self.mostrar_imagen(self.imagen_back)
                self.imagen_actual = "back"
            else:
                self.mostrar_imagen(self.imagen_front)
                self.imagen_actual = "front"

    def preprocesar_imagen(self):
        """ Aplica filtros de procesamiento a ambas imágenes. """
        if not self.imagen_front or not self.imagen_back:
            self.resultado_label.config(text="⚠️ Escanea o carga ambas imágenes primero.", fg="red")
            return

        processed_front = preprocess_image(cv2.imread(self.imagen_front))
        processed_back = preprocess_image(cv2.imread(self.imagen_back))

        self.imagen_front = "processed_front.png"
        self.imagen_back = "processed_back.png"

        cv2.imwrite(self.imagen_front, processed_front)
        cv2.imwrite(self.imagen_back, processed_back)

        self.mostrar_imagen(self.imagen_front)
        self.resultado_label.config(text="✅ Imágenes preprocesadas correctamente.", fg="green")

    def ejecutar_ocr(self):
        """ Ejecuta OCR en ambas imágenes preprocesadas. """
        if not self.imagen_front or not self.imagen_back:
            self.resultado_label.config(text="⚠️ No hay imágenes para procesar.", fg="red")
            return

        datos = process_document(self.imagen_front, self.imagen_back)
        datos_front = datos["Parte Frontal"]
        datos_back = datos["Parte Trasera"]

        resultado_texto = "📝 **Parte Frontal:**\n"
        resultado_texto += f"  Número de Documento: {datos_front.get('Número de Documento', 'No detectado')}\n"
        resultado_texto += f"  Apellidos: {datos_front.get('Apellidos', 'No detectado')}\n"
        resultado_texto += f"  Nombres: {datos_front.get('Nombres', 'No detectado')}\n\n"

        resultado_texto += "📝 **Parte Trasera:**\n"
        resultado_texto += f"  Fecha de nacimiento: {datos_back.get('Fecha de nacimiento', 'No detectado')}\n"
        resultado_texto += f"  Sexo: {datos_back.get('Sexo', 'No detectado')}\n"
        resultado_texto += f"  Lugar de expedición: {datos_back.get('Lugar de expedicion', 'No detectado')}\n"

        self.resultado_label.config(text=resultado_texto, fg="blue")

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
