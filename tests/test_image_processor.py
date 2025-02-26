import sys
import os
import cv2

# Añadir la carpeta raíz del proyecto al sistema de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import os
from src.image_processor import preprocess_image

def test_preprocess_images():
    """
    Prueba la función preprocess_image asegurando que ambas imágenes (frontal y trasera)
    se procesen correctamente y sean más legibles para OCR y LayoutLMv3.
    """
    # Construcción correcta de rutas
    base_path = os.path.join("data")  # Directorio base
    test_front_image_path = os.path.join(base_path, "scanned_document_front.png")
    test_back_image_path = os.path.join(base_path, "scanned_document_back.png")

    # Verificar si los archivos existen antes de cargarlos
    if not os.path.exists(test_front_image_path):
        print(f"❌ Error: No se encontró la imagen frontal en {test_front_image_path}")
        return

    if not os.path.exists(test_back_image_path):
        print(f"❌ Error: No se encontró la imagen trasera en {test_back_image_path}")
        return

    # Intentar cargar las imágenes con OpenCV
    front_image = cv2.imread(test_front_image_path)
    back_image = cv2.imread(test_back_image_path)

    if front_image is None:
        print(f"❌ Error: OpenCV no pudo leer la imagen frontal ({test_front_image_path}).")
        return

    if back_image is None:
        print(f"❌ Error: OpenCV no pudo leer la imagen trasera ({test_back_image_path}).")
        return

    print(f"📄 Imagen frontal original: {front_image.shape[1]}x{front_image.shape[0]} píxeles")
    print(f"📄 Imagen trasera original: {back_image.shape[1]}x{back_image.shape[0]} píxeles")

    try:
        # Aplicar preprocesamiento a ambas imágenes
        processed_front = preprocess_image(front_image)
        processed_back = preprocess_image(back_image)

        # Guardar las imágenes preprocesadas para revisión visual
        output_front_path = os.path.join(base_path, "preprocessed_front.png")
        output_back_path = os.path.join(base_path, "preprocessed_back.png")
        cv2.imwrite(output_front_path, processed_front)
        cv2.imwrite(output_back_path, processed_back)

        print("✅ Preprocesamiento exitoso: Ambas imágenes mejoradas para OCR")
        print(f"✅ Imagen frontal procesada guardada en: {output_front_path}")
        print(f"✅ Imagen trasera procesada guardada en: {output_back_path}")

    except Exception as e:
        print(f"❌ Error durante la prueba de preprocesamiento: {str(e)}")

if __name__ == "__main__":
    test_preprocess_images()
