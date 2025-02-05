import cv2
import numpy as np

# Dimensiones en píxeles basadas en la resolución del escáner
TARGET_WIDTH_MM = 85
TARGET_HEIGHT_MM = 54
SCAN_RESOLUTION_DPI = 600  # Ajusta según la configuración del escáner

# Convertir de mm a píxeles (1 pulgada = 25.4 mm)
TARGET_WIDTH_PX = int((TARGET_WIDTH_MM / 25.4) * SCAN_RESOLUTION_DPI)
TARGET_HEIGHT_PX = int((TARGET_HEIGHT_MM / 25.4) * SCAN_RESOLUTION_DPI)


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Aplica preprocesamiento a la imagen escaneada para mejorar la legibilidad por OCR y LayoutLMv3.

    Args:
        image (np.ndarray): Imagen escaneada en formato OpenCV.

    Returns:
        np.ndarray: Imagen mejorada para OCR.
    """
    try:
        if not isinstance(image, np.ndarray):
            raise ValueError("❌ Error: La entrada a preprocess_image no es una imagen válida.")

        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar un filtro de reducción de ruido
        denoised = cv2.fastNlMeansDenoising(gray, h=50, templateWindowSize=7, searchWindowSize=21)

        # Aplicar binarización adaptativa para mejorar la nitidez del texto
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 3)

        # Aplicar una ligera corrección de contraste
        alpha, beta = 3, 10  # Aumenta el contraste y brillo
        contrast_enhanced = cv2.convertScaleAbs(binary, alpha=alpha, beta=beta)

        return contrast_enhanced
    except Exception as e:
        raise Exception(f"Error en el preprocesamiento de la imagen: {str(e)}")

def save_image(image: np.ndarray, output_path: str) -> None:
    """
    Guarda la imagen procesada en el disco.

    Args:
        image (np.ndarray): Imagen a guardar.
        output_path (str): Ruta donde se guardará la imagen.
    """
    try:
        cv2.imwrite(output_path, image)
    except Exception as e:
        raise Exception(f"Error al guardar la imagen: {str(e)}")
    


def crop_document(image: np.ndarray) -> np.ndarray:
    """
    Recorta la imagen desde la esquina superior izquierda al tamaño exacto de una cédula (85mm x 54mm) a 200 DPI.

    Args:
        image (np.ndarray): Imagen escaneada en formato OpenCV.

    Returns:
        np.ndarray: Imagen recortada con el documento.
    """
    try:
        height, width = image.shape[:2]

        # Verificar si la imagen tiene al menos el tamaño esperado
        if width < TARGET_WIDTH_PX or height < TARGET_HEIGHT_PX:
            raise ValueError("La imagen escaneada es demasiado pequeña para recortar con las dimensiones fijas.")

        # Recortar desde la esquina superior izquierda (0,0)
        cropped_image = image[0:TARGET_HEIGHT_PX, 0:TARGET_WIDTH_PX]

        return cropped_image
    except Exception as e:
        raise Exception(f"Error al recortar la imagen: {str(e)}")