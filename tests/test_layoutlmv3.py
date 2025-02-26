import sys
import os

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import os
from src.ocr.layoutlmv3_processor import process_document, resize_image

def test_process_document():
    """
    Prueba el procesamiento de un documento con imágenes de diferentes tamaños,
    asegurando que sean redimensionadas a 669x425 píxeles antes del OCR.
    """
    base_path = os.path.join("NotarIAG", "data")  # Directorio base
    front_image_path = os.path.join(base_path, "preprocessed_front.png")
    back_image_path = os.path.join(base_path, "preprocessed_back.png")

    # Verificar si los archivos existen
    if not os.path.exists(front_image_path):
        print(f"❌ Error: No se encontró la imagen frontal en {front_image_path}")
        return

    if not os.path.exists(back_image_path):
        print(f"❌ Error: No se encontró la imagen trasera en {back_image_path}")
        return

    # Cargar imágenes
    front_image = cv2.imread(front_image_path)
    back_image = cv2.imread(back_image_path)

    if front_image is None:
        print(f"❌ Error: OpenCV no pudo leer la imagen frontal ({front_image_path}).")
        return

    if back_image is None:
        print(f"❌ Error: OpenCV no pudo leer la imagen trasera ({back_image_path}).")
        return

    # Redimensionar si es necesario
    front_image = resize_image(front_image)
    back_image = resize_image(back_image)

    print(f"📄 Imagen frontal redimensionada: {front_image.shape[1]}x{front_image.shape[0]} píxeles")
    print(f"📄 Imagen trasera redimensionada: {back_image.shape[1]}x{back_image.shape[0]} píxeles")

    try:
        extracted_data = process_document(front_image, back_image)

        print("✅ Extracción de datos exitosa:")
        for section, data in extracted_data.items():
            print(f"\n📝 {section}:")
            for field, value in data.items():
                print(f"  {field}: {value}")

    except Exception as e:
        print(f"❌ Error durante la prueba de procesamiento de documento: {str(e)}")

if __name__ == "__main__":
    test_process_document()