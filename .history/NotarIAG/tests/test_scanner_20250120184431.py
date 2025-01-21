from src.scanner.scanner import scan_document
from src.scanner.image_processor import preprocess_image
from src.ocr.layoutlmv3_processor import extract_zones_from_multiple

def test_scan_document():
    """
    Prueba para escanear un documento con parte frontal y trasera.
    """
    output_front = "data/scanned_document_front.png"
    output_back = "data/scanned_document_back.png"
    try:
        print("Iniciando escaneo de ambas partes...")
        scan_document(output_front, output_back)

        # Preprocesar las imágenes
        preprocessed_front = preprocess_image(output_front)
        preprocessed_back = preprocess_image(output_back)
        print("Imágenes preprocesadas correctamente.")

        # Guardar las imágenes preprocesadas
        preprocess_output_front = "data/preprocessed_front.png"
        preprocess_output_back = "data/preprocessed_back.png"
        preprocess_image(preprocessed_front, preprocess_output_front)
        preprocess_image(preprocessed_back, preprocess_output_back)

        # Aplicar OCR a ambas imágenes
        results = extract_zones_from_multiple([preprocess_output_front, preprocess_output_back])
        print("Resultados del OCR:")
        print(results)
    except Exception as e:
        print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    test_scan_document()
