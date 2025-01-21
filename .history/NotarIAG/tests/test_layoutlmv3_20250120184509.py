import sys
import os

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.ocr.layoutlmv3_processor import process_document

def test_process_document():
    """
    Prueba el procesamiento de un documento con parte frontal y trasera.
    """
    front_image = "NotarIAG/data/scanned_document_front.png"
    back_image = "NotarIAG/data/scanned_document_back.png"
    try:
        results = process_document(front_image, back_image)
        print("Resultados del procesamiento del documento:")
        for part, data in results.items():
            print(f"\n{part}:")
            for field, value in data.items():
                print(f"  {field}: {value}")
    except Exception as e:
        print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    test_process_document()
