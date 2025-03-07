import re
import tkinter as tk
from tkinter import filedialog
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from docx import Document

# Si Tesseract no está en el PATH, descomenta y ajusta la siguiente línea:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
