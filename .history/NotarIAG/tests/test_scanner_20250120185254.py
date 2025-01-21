import sys
import os

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from src.scanner.scanner import scan_document
from src.ocr.layoutlmv3_processor import extract_zones_front, extract_zones_back

def test_scan_document():
    """
    Prueba el escaneo de ambas partes del documento.
    """
    front_image = "NotarIAG/data/scanned_document_front.png"
    back_image = "NotarIAG/data/scanned_document_back.png"
    try:
        print("Iniciando escaneo...")
        scan_document(front_image, back_image)

        # Procesar la parte frontal
        print("\nProcesando la parte frontal:")
        front_data = extract_zones_front(front_image)
        for key, value in front_data.items():
            print(f"  {key}: {value}")

        # Procesar la parte trasera
        print("\nProcesando la parte trasera:")
        back_data = extract_zones_back(back_image)
        for key, value in back_data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    test_scan_document()
