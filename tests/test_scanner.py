import sys
import os


# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from src.scanner.scanner import scan_document

def test_scan_document():
    """
    Prueba el escaneo de ambas partes del documento.
    """
    front_image = "NotarIAG/data/scanned_document_front.png"
    back_image = "NotarIAG/data/scanned_document_back.png"
    try:
        print("Iniciando escaneo de ambas partes del documento...")
        scan_document(front_image, back_image)
        print(f"Parte frontal guardada en: {front_image}")
        print(f"Parte trasera guardada en: {back_image}")
    except Exception as e:
        print(f"Error durante la prueba de escaneo: {e}")

if __name__ == "__main__":
    test_scan_document()