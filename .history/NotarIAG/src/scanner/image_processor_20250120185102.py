import cv2
import numpy as np

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocesa una imagen para mejorar la precisión del OCR.

    Args:
        image_path (str): Ruta de la imagen a preprocesar.

    Returns:
        np.ndarray: Imagen preprocesada.
    """
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen desde {image_path}")
        
        # Reducir ruido
        image = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Umbral adaptativo
        image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return image
    except Exception as e:
        raise Exception(f"Error durante el preprocesamiento: {str(e)}")

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
