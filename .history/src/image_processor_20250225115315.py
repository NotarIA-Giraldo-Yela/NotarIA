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
    min_thickness = 10  # Grosor mínimo
    max_thickness = 80  # Grosor máximo

    try:
        # 1. Binarizar la imagen (si no está binarizada)
        if len(image.shape) == 3:  # Si la imagen es a color, convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

        # 2. Encontrar contornos de los caracteres
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 3. Crear una máscara para los caracteres que cumplen con el grosor
        mask = np.zeros_like(binary)

        for contour in contours:
            # Obtener el rectángulo delimitador del contorno
            x, y, w, h = cv2.boundingRect(contour)

            # Filtrar por grosor (ancho del rectángulo)
            if min_thickness <= w <= max_thickness:
                cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # 4. Aplicar la máscara a la imagen original
        filtered_image = cv2.bitwise_and(binary, binary, mask=mask)

        # 5. Invertir la imagen para que el texto sea negro sobre fondo blanco
        filtered_image = cv2.bitwise_not(filtered_image)

        return filtered_image
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