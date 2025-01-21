import sys
import os

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scanner.image_processor import preprocess_image, save_image
import cv2

def test_preprocess_image():
    """
    Prueba el preprocesamiento de una imagen.
    """
    input_image_path = "NotarIAG/data/scanned_document.png"  # Ruta de la imagen de entrada
    output_image_path = "NotarIAG/data/test_document_processed.png"  # Ruta de la imagen procesada

    try:
        # Preprocesar la imagen
        processed_image = preprocess_image(input_image_path)

        # Guardar la imagen procesada
        save_image(processed_image, output_image_path)
        print(f"Imagen procesada y guardada en: {output_image_path}")

        # Verificar que la imagen procesada exista
        loaded_image = cv2.imread(output_image_path)
        if loaded_image is None:
            print("Error: No se pudo cargar la imagen procesada.")
        else:
            print("La imagen procesada se guardó y cargó correctamente.")
    except Exception as e:
        print(f"Error durante la prueba de preprocesamiento: {str(e)}")

if __name__ == "__main__":
    test_preprocess_image()
