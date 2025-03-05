import re
import tkinter as tk
from tkinter import filedialog
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from docx import Document

# Si Tesseract no está en el PATH, descomenta y ajusta la siguiente línea:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

def update_docx_template(docx_path, output_path, extracted_data):
    """
    Abre la plantilla DOCX, busca las líneas que contienen los títulos
    y reemplaza su contenido con los datos extraídos:
      - Matrícula Inmobiliaria
      - Cédula Catastral (se combinan los dos campos si existen)
      - Ubicación del Predio
      - Dirección del Inmueble
    Guarda el documento actualizado en 'output_path'.
    """
    doc = Document(docx_path)
    # Procesar la Cédula Catastral como un único string
    cedula_catastral_str = ""
    cc = extracted_data.get("cedula_catastral", {})
    if cc.get("CODIGO_CATASTRAL") and cc.get("COD_CATASTRAL_ANT"):
        cedula_catastral_str = f"{cc.get('CODIGO_CATASTRAL')} / {cc.get('COD_CATASTRAL_ANT')}"
    elif cc.get("CODIGO_CATASTRAL"):
        cedula_catastral_str = cc.get("CODIGO_CATASTRAL")
    elif cc.get("COD_CATASTRAL_ANT"):
        cedula_catastral_str = cc.get("COD_CATASTRAL_ANT")
    
    for paragraph in doc.paragraphs:
        if "Matrícula Inmobiliaria:" in paragraph.text:
            paragraph.text = f"Matrícula Inmobiliaria: {extracted_data.get('matricula', '')}"
        if "Cédula Catastral:" in paragraph.text:
            paragraph.text = f"Cédula Catastral: {cedula_catastral_str}"
        if "Ubicación del Predio:" in paragraph.text:
            paragraph.text = f"Ubicación del Predio: {extracted_data.get('ubicacion_predio', '')}"
        if "Dirección del Inmueble:" in paragraph.text:
            paragraph.text = f"Dirección del Inmueble: {extracted_data.get('direccion_inmueble', '')}"
    doc.save(output_path)

def PDf_read (pdf_path):
    
    if pdf_path:
        matricula = extract_first_matricula_from_pdf(pdf_path)
        cedula_catastral = extract_cedula_catastral_from_pdf(pdf_path)
        ubicacion_predio = extract_ubicacion_predio_from_pdf(pdf_path)
        direccion_inmueble = extract_direccion_inmueble_from_pdf(pdf_path)
        
        if matricula:
            print("Número de matrícula encontrado:")
            print(matricula)
            print("\nVariable alfanumérica con el resultado (Matrícula):", matricula)
        else:
            print("No se encontró ningún número de matrícula en el PDF.")
        
        if cedula_catastral["CODIGO_CATASTRAL"] or cedula_catastral["COD_CATASTRAL_ANT"]:
            print("\nCédula Catastral encontrada:")
            print(cedula_catastral)
        else:
            print("No se encontró la Cédula Catastral en el PDF.")
        
        if ubicacion_predio:
            print("\nUbicación del predio (CIRCULO REGISTRAL) encontrada:")
            print(ubicacion_predio)
        else:
            print("No se encontró la Ubicación del predio en el PDF.")
        
        if direccion_inmueble:
            print("\nDirección del inmueble encontrada:")
            print(direccion_inmueble)
        else:
            print("No se encontró la Dirección del inmueble en el PDF.")
        
        # Ahora, solicitar la plantilla DOCX para insertar los datos extraídos
        docx_path = filedialog.askopenfilename(
            title="Selecciona la plantilla DOCX",
            filetypes=[("Documentos DOCX", "*.docx")]
        )
        
        if docx_path:
            extracted_data = {
                "matricula": matricula,
                "cedula_catastral": cedula_catastral,
                "ubicacion_predio": ubicacion_predio,
                "direccion_inmueble": direccion_inmueble
            }
            output_docx = "Documento_Actualizado.docx"
            update_docx_template(docx_path, output_docx, extracted_data)
            print(f"\nEl documento actualizado se ha guardado como: {output_docx}")
        else:
            print("No se seleccionó ningún archivo DOCX para la plantilla.")

        return{
            "matricula": matricula,
            "cedula_catastral": cedula_catastral,
            "ubicacion_predio": ubicacion_predio,
            "direccion_inmueble": direccion_inmueble
        }    
    else:
        print("No se seleccionó ningún archivo PDF.")

