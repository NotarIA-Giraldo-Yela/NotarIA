import sys
import os

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocr.layoutlmv3_processor import extract_zones

def test_extract_zones():
    """
    Prueba la extracción de datos por zonas en un documento.
    """
    image_path = "NotarIAG/data/test_document_processed.png"  # Ruta de la imagen procesada
    try:
        # Extraer datos de las zonas
        result = extract_zones(image_path)
        print("Datos Extraídos por Zonas:")
        for key, value in result.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error durante la prueba de extracción por zonas: {str(e)}")

if __name__ == "__main__":
    test_extract_zones()
