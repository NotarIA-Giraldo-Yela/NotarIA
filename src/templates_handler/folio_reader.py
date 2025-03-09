import re
import tkinter as tk
from tkinter import ttk
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from docx import Document

# Si Tesseract no está en el PATH, descomenta y ajusta la siguiente línea:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def show_progress():
    """ Crea una ventana emergente con una barra de carga. """
    root = tk.Toplevel()
    root.title("Procesando documento")
    root.geometry("400x150")  # Tamaño de la ventana
    root.resizable(False, False)

    ttk.Label(root, text="Procesando documento, por favor espere...", font=("Arial", 12)).pack(pady=10)
    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)
    
    return root, progress

def extract_first_matricula_from_pdf(pdf_path):
    """Extrae el primer número de matrícula encontrado en el PDF."""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                matches = re.findall(r"[Mm]atr[ií]cula\s*[:\-]?\s*([\w\d-]+)", text)
                if matches:
                    return matches[0]
    # Si no se encuentra con PyPDF2, se intenta con OCR
    images = convert_from_path(pdf_path)
    for image in images:
        text = pytesseract.image_to_string(image, lang='spa')
        matches = re.findall(r"[Mm]atr[ií]cula\s*[:\-]?\s*([\w\d-]+)", text)
        if matches:
            return matches[0]
    return None

def extract_cedula_catastral_from_pdf(pdf_path):
    """
    Busca en el documento los campos "CODIGO CATASTRAL" y "COD CATASTRAL ANT".
    - Permite variaciones como "COD. CATASTRAL", "ANT.", etc.
    - Captura también cadenas con espacios (p.ej. "SIN INFORMACION").
    - Si el resultado de CODIGO CATASTRAL termina con "COD", se elimina.
    - Si el resultado de CODIGO CATASTRAL contiene "COD CATASTRAL ANT" (o variaciones),
      se recorta para no arrastrar información del siguiente campo.
    El resultado se almacena en un diccionario llamado cedula_catastral.
    """
    codigo_catastral = None
    codigo_catastral_ant = None

    # Intentar extraer con PyPDF2
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                # ------------------------
                # CODIGO CATASTRAL
                # ------------------------
                if codigo_catastral is None:
                    match1 = re.search(
                        r"CODIGO\.?\s*CATASTRAL\.?\s*[:\-]?\s*([\w\d\s.-]+)",
                        text,
                        re.IGNORECASE
                    )
                    if match1:
                        codigo_catastral_temp = match1.group(1)
                        codigo_catastral_temp = codigo_catastral_temp.split("\n", 1)[0].strip()
                        buscar_ant = re.search(
                            r"COD\.?\s*CATASTRAL\.?\s*ANT\.?",
                            codigo_catastral_temp,
                            re.IGNORECASE
                        )
                        if buscar_ant:
                            start_index = buscar_ant.start()
                            codigo_catastral_temp = codigo_catastral_temp[:start_index].strip()
                        if len(codigo_catastral_temp) >= 3 and codigo_catastral_temp[-3:].upper() == "COD":
                            codigo_catastral_temp = codigo_catastral_temp[:-3].strip()
                        codigo_catastral = codigo_catastral_temp

                # ------------------------
                # COD CATASTRAL ANT
                # ------------------------
                if codigo_catastral_ant is None:
                    match2 = re.search(
                        r"COD\.?\s*CATASTRAL\.?\s*ANT\.?\s*[:\-]?\s*([\w\d\s.-]+)",
                        text,
                        re.IGNORECASE
                    )
                    if match2:
                        codigo_catastral_ant_temp = match2.group(1)
                        codigo_catastral_ant_temp = codigo_catastral_ant_temp.split("\n", 1)[0].strip()
                        codigo_catastral_ant = codigo_catastral_ant_temp

            if codigo_catastral is not None and codigo_catastral_ant is not None:
                break

    if codigo_catastral is None or codigo_catastral_ant is None:
        images = convert_from_path(pdf_path)
        for image in images:
            text = pytesseract.image_to_string(image, lang='spa')
            if codigo_catastral is None:
                match1 = re.search(
                    r"CODIGO\.?\s*CATASTRAL\.?\s*[:\-]?\s*([\w\d\s.-]+)",
                    text,
                    re.IGNORECASE
                )
                if match1:
                    codigo_catastral_temp = match1.group(1)
                    codigo_catastral_temp = codigo_catastral_temp.split("\n", 1)[0].strip()
                    buscar_ant = re.search(
                        r"COD\.?\s*CATASTRAL\.?\s*ANT\.?",
                        codigo_catastral_temp,
                        re.IGNORECASE
                    )
                    if buscar_ant:
                        start_index = buscar_ant.start()
                        codigo_catastral_temp = codigo_catastral_temp[:start_index].strip()
                    if len(codigo_catastral_temp) >= 3 and codigo_catastral_temp[-3:].upper() == "COD":
                        codigo_catastral_temp = codigo_catastral_temp[:-3].strip()
                    codigo_catastral = codigo_catastral_temp
            if codigo_catastral_ant is None:
                match2 = re.search(
                    r"COD\.?\s*CATASTRAL\.?\s*ANT\.?\s*[:\-]?\s*([\w\d\s.-]+)",
                    text,
                    re.IGNORECASE
                )
                if match2:
                    codigo_catastral_ant_temp = match2.group(1)
                    codigo_catastral_ant_temp = codigo_catastral_ant_temp.split("\n", 1)[0].strip()
                    codigo_catastral_ant = codigo_catastral_ant_temp
            if codigo_catastral is not None and codigo_catastral_ant is not None:
                break

    cedula_catastral = {
        "CODIGO_CATASTRAL": codigo_catastral,
        "COD_CATASTRAL_ANT": codigo_catastral_ant
    }
    return cedula_catastral

def extract_ubicacion_predio_from_pdf(pdf_path):
    """
    Busca en el documento la línea que contiene "CIRCULO REGISTRAL:" y
    extrae todo el contenido hasta el siguiente salto de línea.
    Retorna el texto encontrado o None si no aparece.
    """
    ubicacion_predio = None
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                match = re.search(
                    r"CIRCULO\s+REGISTRAL\s*[:\-]?\s*([^\n]+)",
                    text,
                    re.IGNORECASE
                )
                if match:
                    ubicacion_temp = match.group(1).strip()
                    ubicacion_predio = ubicacion_temp
                    break
    if ubicacion_predio is None:
        images = convert_from_path(pdf_path)
        for image in images:
            text = pytesseract.image_to_string(image, lang='spa')
            match = re.search(
                r"CIRCULO\s+REGISTRAL\s*[:\-]?\s*([^\n]+)",
                text,
                re.IGNORECASE
            )
            if match:
                ubicacion_temp = match.group(1).strip()
                ubicacion_predio = ubicacion_temp
                break
    return ubicacion_predio

def extract_direccion_inmueble_from_pdf(pdf_path):
    """
    Busca en el documento la sección "DESCRIPCION: CABIDA Y LINDEROS" y
    extrae todo el párrafo que sigue.
    Se detiene si encuentra "COMPLEMENTACION" y no lo incluye.
    El resultado se guarda en la variable "Dirección del inmueble".
    """
    direccion_inmueble = None
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                match = re.search(
                    r"DESCRIPCION\s*[:\-]?\s*CABIDA\s+Y\s+LINDEROS\s*[:\-]?\s*([\w\W]+?)(?:\n\s*\n|$)",
                    text,
                    re.IGNORECASE
                )
                if match:
                    direccion_temp = match.group(1).strip()
                    m_complementacion = re.search(r"COMPLEMENTACION", direccion_temp, re.IGNORECASE)
                    if m_complementacion:
                        direccion_temp = direccion_temp[:m_complementacion.start()].strip()
                    direccion_inmueble = direccion_temp
                    break
    if direccion_inmueble is None:
        images = convert_from_path(pdf_path)
        for image in images:
            text = pytesseract.image_to_string(image, lang='spa')
            match = re.search(
                r"DESCRIPCION\s*[:\-]?\s*CABIDA\s+Y\s+LINDEROS\s*[:\-]?\s*([\w\W]+?)(?:\n\s*\n|$)",
                text,
                re.IGNORECASE
            )
            if match:
                direccion_temp = match.group(1).strip()
                m_complementacion = re.search(r"COMPLEMENTACION", direccion_temp, re.IGNORECASE)
                if m_complementacion:
                    direccion_temp = direccion_temp[:m_complementacion.start()].strip()
                direccion_inmueble = direccion_temp
                break
    return direccion_inmueble

def PDf_read(pdf_path):
    """ Lee un archivo PDF y extrae los datos relevantes con una barra de progreso. """
    
    if not pdf_path:
        print("No se seleccionó ningún archivo PDF.")
        return None

    # Crear la ventana de progreso
    progress_window, progress = show_progress()
    progress_window.update()

    steps = 4  # Número de pasos en el proceso
    progress_step = 100 / steps  # Incremento por cada paso

    try:
        matricula = extract_first_matricula_from_pdf(pdf_path)
        progress["value"] += progress_step
        progress_window.update()

        cedula_catastral = extract_cedula_catastral_from_pdf(pdf_path)
        progress["value"] += progress_step
        progress_window.update()

        ubicacion_predio = extract_ubicacion_predio_from_pdf(pdf_path)
        progress["value"] += progress_step
        progress_window.update()

        direccion_inmueble = extract_direccion_inmueble_from_pdf(pdf_path)
        progress["value"] += progress_step
        progress_window.update()

        # Cerrar la ventana de progreso después de completar todas las tareas
        progress_window.destroy()

        # Mostrar los resultados en la terminal
        if matricula:
            print("\nNúmero de matrícula encontrado:", matricula)
        else:
            print("No se encontró ningún número de matrícula en el PDF.")
        
        if cedula_catastral["CODIGO_CATASTRAL"] or cedula_catastral["COD_CATASTRAL_ANT"]:
            print("\nCédula Catastral encontrada:", cedula_catastral)
        else:
            print("No se encontró la Cédula Catastral en el PDF.")
        
        if ubicacion_predio:
            print("\nUbicación del predio encontrada:", ubicacion_predio)
        else:
            print("No se encontró la Ubicación del predio en el PDF.")
        
        if direccion_inmueble:
            print("\nDirección del inmueble encontrada:", direccion_inmueble)
        else:
            print("No se encontró la Dirección del inmueble en el PDF.")
        
        return {
            "matricula": matricula,
            "cedula_catastral": cedula_catastral,
            "ubicacion_predio": ubicacion_predio,
            "direccion_inmueble": direccion_inmueble
        }

    except Exception as e:
        progress_window.destroy()  # Asegurar que la ventana de progreso se cierre en caso de error
        raise Exception(f"Error al procesar el documento: {str(e)}")

